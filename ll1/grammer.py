from functools import reduce 

alphabet = ""
for i in range(ord('a'), ord('z') + 1):
    alphabet += chr(i)

is_terminal = lambda c: ord('a') <= ord(c) <= ord('z')

def eliminate_left_recursion(grammar):
    """
    if we have a rule like:
    A -> AX | Y
    we should convert it to:
    A -> YA'
    A' -> XA' | ε
    """

    grammar_non_terminals = list(grammar.keys())
    available_non_terminals = list(set(alphabet.upper()) - set(grammar.keys()))
    
    has_left_recursion = lambda symbol: any([i.startswith(symbol) for i in grammar[symbol]])

    for nt in grammar_non_terminals:
        if not has_left_recursion(nt):
            continue
        helper_nt = available_non_terminals.pop()
        nt_products = []
        helper_products = [""]
        for product in grammar[nt]:
            if product.startswith(nt): # A -> AX => A' -> XA' 
                helper_products.append(product[len(nt):] + helper_nt)
            else: # A -> Y => A -> YA'
                nt_products.append(product + helper_nt)
        grammar[nt] = nt_products
        grammar[helper_nt] = helper_products
    return grammar


def first(grammer, symbol, visited = None):
    """
    if we have rule: A -> aB, C, bD, KJ then first(A) = {a, b} + first(C) + first(K) (if K is nullable, then we must add its follow to) 
    """

    if visited is None:
        visited = set()
    visited.add(symbol)

    ans = set()
    for product in grammer[symbol]:
        if not product:
            ans.add("")
            continue

        char = product[0]
        if char in visited:
            continue

        if is_terminal(char):
            ans.add(char)
        else:
            res = first(grammer, char, visited=visited)
            ans = ans.union(res)
            p_ind = 1
            while "" in res and p_ind < len(product):
                char = product[p_ind]
                res = first(grammer, char)
                ans = ans.union(res)
                ans.remove("")
            if p_ind == len(product):
                ans.add("")

    return ans 

def follow(grammar, symbol, visited = set()):
    """
    we must return all b's that we have in a form in: s->* XAbC for follow(A)
    """
    products = list(grammar.values())
    products = reduce(lambda a, b: a + b, products)
    
    ans = set() 
    for p in products: 
        if not symbol in p:
            continue 
        last_index = 0
        for _ in range(p.count(symbol)):
            last_index = p.index(symbol, last_index) + 1
            if last_index == len(p):
                continue 
            nxt = p[last_index] 
            if is_terminal(nxt):
                ans.add(nxt)
            else:
                res = first(grammar, nxt)
                ans = ans.union(res)
                ind = last_index + 1
                while "" in res and ind < len(p):
                    char = p[ind]
                    res = first(grammar, char)
                    ans = ans.union(res)
                    ind += 1
                if ind == len(p):
                    ans.add("")
                else:
                    ans.remove("")

    return ans

def find_follow(grammar, symbol, terminal, visited = None):
    """
    terminal must be part of first(symbol)
    this function will find all X so that we have 'symbol -> terminal X' 
    """

    if visited is None:
        visited = set()
    visited.add(symbol)

    ans = set()
    for product in grammar[symbol]:
        if not product:
            continue

        char = product[0]
        if char in visited:
            continue

        if char == terminal:
            ans.add(product[1:])
            continue
        if is_terminal(char):
            continue



        ind = 0
        res = first(grammar, product[ind], visited=visited)
        while "" in res and ind < len(product):
            if terminal in res:
                ans = ans.union(find_follow(grammar, product[ind], terminal))
            ind += 1
            if ind < len(product):
                res = first(grammar, product[ind], visited=visited)


    return ans 


def remove_left_common(grammar):
    available_non_terminals = list(set(alphabet) - set(grammar.keys()))
    new_grammer = {}
    while len(grammar) != len(new_grammer): 
        if new_grammer:
            grammar = new_grammer.copy()
            new_grammer = {}.copy()

        for nt in grammar.keys():
            try:
                new_nt = available_non_terminals.pop()
            except:
                return grammar
            
            for char in first(grammar, nt):
                new_grammer[nt] = [f"{char}{new_nt}"]
                new_grammer[new_nt] = list(find_follow(grammar, nt, char))
            
        
def factorize_grammar():
    new_grammar = {}
    for non_terminal, productions in grammar.items():
        new_grammar[non_terminal] = []
        while len(productions) > 0:
            current_production = productions.pop(0)
            common_prefix = ''
            for production in productions[:]:
                while common_prefix != production[:len(common_prefix)]:
                    common_prefix = common_prefix[:-1]
                while current_production != current_production[:len(common_prefix)]:
                    common_prefix = common_prefix[:-1]
            if common_prefix:
                new_non_terminal = non_terminal + "'"
                new_grammar[new_non_terminal] = [production[len(common_prefix):] for production in [current_production] + productions]
                new_grammar[non_terminal].append(common_prefix + new_non_terminal)
            else:
                new_grammar[non_terminal].append(current_production)
        if not new_grammar[non_terminal]:
            del new_grammar[non_terminal]
    return new_grammar

def convert_to_ll1(grammar):
    grammar = eliminate_left_recursion(grammar)
    grammar = remove_left_common(grammar)
    # grammar = factorize_grammar(grammar)
    return grammar

# Example input grammar
grammars = [
{
        'S': ['aA', 'aB'],
        'A': ['x'],
        'B': ['y'],
    }
]


for i in range(len(grammars)):
    g = convert_to_ll1(grammars[i])
    for k in  g:
        print(f"for non terminal {k} first set is {first(g, k)} and follow set is {follow(g, k)}")
    print(g)
    print()

