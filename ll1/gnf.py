def cfg_to_gnf(cfg):
    """
    Convert a context-free grammar in Chomsky Normal Form to Greibach Normal Form.
    
    Args:
        cfg (dict): The context-free grammar in the form of a dictionary, where the keys are non-terminal symbols
                    and the values are lists of production rules.
    
    Returns:
        dict: The equivalent grammar in Greibach Normal Form.
    """
    gnf_grammar = {}
    
    # Step 1: Eliminate unit productions
    cfg = eliminate_unit_productions(cfg)
    
    # Step 2: Convert to GNF
    for A in cfg:
        gnf_grammar[A] = []
        for rule in cfg[A]:
            if len(rule) == 1 and rule[0] in cfg:
                # A -> B rule, where B is a non-terminal
                for B_rule in cfg[rule[0]]:
                    gnf_grammar[A].append([rule[0]] + B_rule)
            else:
                # A -> a... or A -> aB... rule
                gnf_grammar[A].append(rule)
    
    return gnf_grammar

def eliminate_unit_productions(cfg):
    """
    Eliminate unit productions from a context-free grammar in Chomsky Normal Form.
    
    Args:
        cfg (dict): The context-free grammar in the form of a dictionary, where the keys are non-terminal symbols
                    and the values are lists of production rules.
    
    Returns:
        dict: The CFG with unit productions eliminated.
    """
    new_cfg = {}
    
    for A in cfg:
        new_cfg[A] = []
        for rule in cfg[A]:
            if len(rule) == 1 and rule[0] in cfg:
                # A -> B rule, where B is a non-terminal
                for B_rule in cfg[rule[0]]:
                    new_cfg[A].append(B_rule)
            else:
                new_cfg[A].append(rule)
    
    return new_cfg


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
    gnf_grammar = cfg_to_gnf(g)
    print(gnf_grammar)