alphabet = ""
for i in range(ord('a'), ord('z') + 1):
    alphabet += chr(i)

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
    if visited is None:
        visited = set()
    if symbol in visited:
        raise ValueError(f"There is a loop in grammar! {symbol = }, {visited = }")
    visited.append(symbol)

    is_terminal = lambda c: ord('a') <= ord(c) <= ord('z')
    ans = set()
    for product in grammer[symbol]:
        char = product[0]
        if is_terminal(char):
            ans.add(char)
        else:
            ans.add(first())

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
    print(ll1_grammar)

