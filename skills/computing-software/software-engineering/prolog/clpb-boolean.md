---
id: computing-software.software-engineering.prolog.clpb-boolean
name: clpb-boolean
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-clp-other, clpb-boolean, sat-count]
level: advanced
status: draft
description: "Solve SAT-style problems with library(clpb): sat/1, taut/2, labeling/1 and sat_count/2."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CLP(B)
```prolog
:- use_module(library(clpb)).
?- sat(X + Y), sat(~X), labeling([X,Y]).     % X=0, Y=1
?- taut(X + ~X, T).                            % T = 1
?- sat_count(A + B + C, N).                    % N = 7
?- sat(card([2], [A,B,C])), labeling([A,B,C]).
```
Operators: `~` not, `+` or, `*` and, `#` xor, `=:=` equivalence, `=<` implication, `card(Is, Es)` cardinality.
## Gotchas
- Variables must be Boolean; use `X in 0..1` conflicts with clpfd only if mixed deliberately.
- BDD size can explode on hard instances.
## Self-check
Encode a 3-colouring of a triangle and count solutions with `sat_count`.
