# LL1 converter 
this project tries to convert a grammar into LL1 form.
## eliminate_left_recursion
first step is to remove the left recursion from the grammar.
we do this by using the formula specified in comments. 
```
A -> AX | Y
convert to:
A -> YA'
A' -> XA' | ε
```
we use extra non terminals to achieve this.
## first and follow
we define first(A) as a set of first terminals we can derviate from A (A is non terminal)
we define follow(A) as all y's that we have `S =>* AyX`.
there is a visited set to avoid infinite loops. because we use recursive call to find first and follow set.
## find_follow
now assume `x` is in `first(A)`. so we know that we can have a rule like `A -> xX` where `X` can be a set of non terminals and terminals. 
so what `find follow` does is to find all possible values for `X`. so later we can simplify grammar by these formula:
```
A -> aB | aC | aD | bc | E (a is not in first(E))
converts to (note that find_follow(A, a) = {B, C, D}):
A -> aX | bc | E
X -> B, C, D
```
## get_trouble_nts
it iterate over all non terminals of grammar and check if we have undeterminicity for a non terminal and return all non terminals that are not deterministic. if there isn't any, then our grammar is ll1. else we try to simplify them using `find_follow`.
## remove_left_common
it tries to simplify grammar by making all non terminals deterministic. 
so it has a recursive call until the output of `get_trouble_nts` is empty. 
## remove dummy non terminals
the grammar my generate some rules like `A -> []` in some corner cases.
it doesn't make grammar incorrect but it is a bit lame to show products like this. more than this, since we add more non terminals to make our grammar ll1, it is important that we don't waste any non terminal.

so this function tries to remove dummy and unit rules to free some non terminals.
## convert to ll1 
it just calls `eliminate_left_recursion` and `remove_left_common` on the grammar.
## simplize 
since we may add many more non terminals, some of them might be unneccessary. so by calling simplize we try to make grammar more consise and avoid any unneccessary states.
it
it does its work by making `reach` and `term` set and then just keep non terminals that are both reachable and terminable.
it doesn't chage a grammar to make it more like ll1 or less, it just helps with time complexity and also output a nicer grammar.

## final 
by calling `convert to ll1 ` and the `simplize` we can have nice compact ll1 grammars. 
the only danger is that since it has a maximum non terminal count as 28, if we need more non terminals, it cannot convert it to ll1 grammar.