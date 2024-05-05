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
    # if visited is None:
    #     visited = set()
    # if symbol in visited:
    #     raise ValueError(f"There is a loop in grammar! {symbol = }, {visited = }")
    # visited.append(symbol)

    ans = set()
    for product in grammer[symbol]:
        char = product[0]
        if is_terminal(char):
            ans.add(char)
        else:
            # ans.add(first(grammar, char, visited))
            ans.add(first(grammar, char))
            #TODO: support nullable nt 

    return ans 

def follow(grammar, symbol, visited = None):
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
        for i in range(p.count(symbol)):
            last_index = p.index(nt, last_index) + 1
            if last_index == len(p):
                continue 
            nxt = p[last_index] 
            if is_terminal(nxt):
                ans.add(nxt)
            else:
                ans.add(first(grammar, symbol))
    return ans

def factorize_grammar(grammar):
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
    follow(grammar, 'A')
    # grammar = factorize_grammar(grammar)
    return grammar

# Example input grammar
grammars = [
    {
        'S': ['Sa', 'b', 'c'],
        'A': ['Ab', 'a', 'S']
    }, {
        'S': ['aB', 'bA', ''],
        'A': ['aS', 'bAA'],
        'B': ['b'],
    }, {
        'S': ['Sa', 'Sb', 'c', 'd']
    }
]

for g in grammars:
    ll1_grammar = convert_to_ll1(g)
    # print(ll1_grammar)

