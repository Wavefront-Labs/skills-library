---
id: computing-software.software-engineering.prolog.dif-constraint
name: dif-constraint
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-pure, dif-constraint, pure-monotonic]
level: practitioner
status: draft
description: "Replace \\= and \\== with dif/2 to keep predicates relational, and write pure monotonic programs that survive goal reordering."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# dif/2 and pure Prolog
```prolog
all_different([]).
all_different([X|Xs]) :- maplist(dif(X), Xs), all_different(Xs).
?- dif(X, a), X = b.        % true
?- dif(X, a), X = a.        % false
?- dif(f(X,Y), f(1,2)), X = 1.   % residual dif(Y,2)
list_without([], _, []).
list_without([X|Xs], E, Ys) :- ( X = E -> Ys = Ys1 ; Ys = [X|Ys1] ), list_without(Xs, E, Ys1).
```
Prefer `if_/3` from library(reif) (pack) or `dif/2` over `->` with unbound variables, to keep the predicate monotonic.
## Gotchas
- `\=` is not monotonic: `X \= a, X = a` and `X = a, X \= a` differ.
- `dif/2` leaves residual goals: view with `copy_term/3`.
- Avoid `var/1`, `nonvar/1` and `!` in code meant to be pure.
## Self-check
Check goal-order independence: both `dif(X,a), X=a` and `X=a, dif(X,a)` must fail.
