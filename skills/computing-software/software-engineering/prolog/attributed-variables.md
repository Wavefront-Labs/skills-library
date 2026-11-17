---
id: computing-software.software-engineering.prolog.attributed-variables
name: attributed-variables
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, attributed-variables, put-attr]
level: sme
status: draft
description: "Implement constraint domains with put_attr/3, get_attr/3 and the attr_unify_hook/2 and attribute_goals//1 hooks."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Attributed variables
```prolog
:- module(domain, [domain/2]).
domain(X, Dom) :- var(Dom), !, get_attr(X, domain, Dom).
domain(X, List) :- list_to_ord_set(List, Domain), put_attr(Y, domain, Domain), X = Y.
attr_unify_hook(Domain, Y) :-
    (   get_attr(Y, domain, Dom2) -> ord_intersection(Domain, Dom2, NewDomain),
        ( NewDomain == [] -> fail ; NewDomain = [Value] -> Y = Value ; put_attr(Y, domain, NewDomain) )
    ;   var(Y) -> put_attr(Y, domain, Domain)
    ;   ord_memberchk(Y, Domain) ).
attribute_goals(X) --> { get_attr(X, domain, List) }, [domain(X, List)].
```
The module name is the attribute key; `attr_unify_hook(AttValue, Other)` runs after unification.
## Gotchas
- The hook runs after binding, not before; failing undoes the unification.
- Implement `attribute_goals//1` so `copy_term/3` and the toplevel show residual goals.
## Self-check
Run `domain(X,[a,b]), domain(X,[b,c])` and confirm X = b.
