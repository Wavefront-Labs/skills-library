---
id: computing-software.software-engineering.prolog.clpfd-labeling
name: clpfd-labeling
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-clpfd, clpfd-labeling, clpfd-domains]
level: practitioner
status: draft
description: "Declare finite domains with in/ins, post arithmetic constraints with #=, #<, #\\= and search with label/1 and labeling/2."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CLP(FD) basics
```prolog
:- use_module(library(clpfd)).
?- X #= 3 + 4.                       % X = 7 (reversible)
?- 7 #= X + 4.                       % X = 3
?- X in 1..5, X #> 3.                % X in 4..5
?- [X,Y] ins 0..9, X + Y #= 10, X #< Y, label([X,Y]).
?- length(L, 3), L ins 1..3, all_different(L), label(L).
?- X #> 3, X #< 6, indomain(X).
```
- Posting constraints narrows domains; `label/1` enumerates; `labeling([ff, down], Vs)` picks heuristics.
- Use `#=` instead of `is` in new code for pure, bidirectional arithmetic.
## Gotchas
- Unbounded variables with `label/1` throw "Arguments are not sufficiently instantiated": give finite domains.
- Residual constraints show at the toplevel; use `copy_term/3` or `fd_dom/2`.
- Do not mix `is` and `#=` on the same variables before labeling.
## Self-check
Solve `X*Y #= 12, X #> 1, Y #> 1, [X,Y] ins 0..12` and list all answers.
