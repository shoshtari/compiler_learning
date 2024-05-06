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
            if "" in res and p_ind == len(product):
                ans.add("")
    return ans 

def follow(grammar, symbol):
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

def remove_dummy_non_terminals(grammar):
    dummies = set() 
    for nt in grammar:
        if len(grammar[nt]) == 1 and '' in grammar[nt]:
            dummies.add(nt)

    new_grammar = {}
    for nt in grammar:
        if nt in dummies:
            continue
        new_grammar[nt] = []
        for p in grammar[nt]:
            new_p = p 
            for d in dummies:
                new_p = new_p.replace(d, '')
            new_grammar[nt].append(new_p)
    return new_grammar

def get_trouble_nts(grammar):
    ans = set()
    for nt in grammar:
        if not all([len(p) == 0 or is_terminal(p[0]) for p in grammar[nt]]):
            ans.add(nt)
    return list(ans)

def remove_left_common(grammar, chars = None):
    available_non_terminals = list(set(alphabet.upper()) - set(grammar.keys()))
    new_grammer = {}

    if chars is None:
        chars = list(grammar.keys())

    for nt in grammar.keys():
        if nt not in chars:
            new_grammer[nt] = grammar[nt].copy()
            continue

        try:
            new_nt = available_non_terminals.pop()
        except:
            return grammar
        
        new_grammer[nt] = []
        for char in first(grammar, nt):
            new_product = list(find_follow(grammar, nt, char))
            if len(new_product) == 0:
                new_grammer[nt].append(char)
            else:
                new_grammer[nt].append(f"{char}{new_nt}")
                new_grammer[new_nt] = new_product
    new_grammer = remove_dummy_non_terminals(new_grammer)
    troubles = get_trouble_nts(new_grammer)
    if len(troubles) == 0:
        return new_grammer
    return remove_left_common(new_grammer, chars = troubles)

            

def convert_to_ll1(grammar):
    grammar = eliminate_left_recursion(grammar)
    grammar = remove_left_common(grammar)
    return grammar

def simplize(grammar, start = 'S'):
    reach = set() 
    term = set()

    # reach
    reach.add(start)
    products = grammar[start].copy()
    while products:
        product = products.pop()
        for char in product:
            if not is_terminal(char):
                reach.add(char)
    
    # term 
    is_all_terminal = lambda s: all([is_terminal(c) or c in term for c in s])
    products = []
    for nt in grammar:
        for product in grammar[nt]:
            if is_all_terminal(product):
                term.add(nt)
    last_term = None 
    while last_term != term:
        last_term = term.copy()
        for nt in grammar:
            for product in grammar[nt]:
                if is_all_terminal(product):
                    term.add(nt)

    # pruning grammar 
    new_grammar = {}
    for nt in grammar:
        if nt not in reach or nt not in term:
            continue
        new_grammar[nt] = []
        for p in grammar[nt]:
            if is_all_terminal(p):
                new_grammar[nt].append(p)
    return new_grammar
    
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
    g = simplize(g)
    for k in  g:
        print(f"for non terminal {k} first set is {first(g, k)} and follow set is {follow(g, k)}")
    print(g)
    print()

