# LL1 converter 
this project tries to convert a grammar into LL1 form.
first step is to remove the left recursion from the grammar.
we do this by using the formula specified in comments. 
we use extra non terminals to achieve this.
then we want to remove common prefix to make our grammar deterministic. 
we do it by using a simple idea! assume that `a` is in the first set of `A`. so we know there is some transition like `A -> a X` where `X` can be some non terminals. so in each step we try to make non terminals of grammar deterministic. but by doing this, we make some new undeterministic non terminals. but hopefully their count is lower than the original grammar. 
so we keep simplifying grammar till we add no more non terminals and then we return the grammar.