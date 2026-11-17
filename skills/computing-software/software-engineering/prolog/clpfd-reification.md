---
id: computing-software.software-engineering.prolog.clpfd-reification
name: clpfd-reification
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, clpfd-reification, all-distinct]
level: advanced
status: draft
description: "Use all_distinct/1, sum/3, tuples_in/2, element/3, circuit/1, cumulative/2 and reified constraints #<==>, #==> and #\\/."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Global constraints and reification
```prolog
?- Vs = [A,B,C], Vs ins 1..3, all_distinct(Vs), A #< B, B #< C.
?- sum([X,Y,Z], #=, 10).
?- element(I, [10,20,30], V).
?- tuples_in([[X,Y]], [[1,2],[2,3],[3,1]]).
?- B #<==> (X #> 3), X in 0..5.         % reify into boolean
?- X in 0..9, (X #< 3 #\/ X #> 7).
?- circuit([S1,S2,S3]).
```
- `all_distinct/1` propagates more strongly than `all_different/1`.
- `#<==>`, `#==>`, `#\/`, `#/\`, `#\` combine reified constraints.
## Gotchas
- Reification of non-reifiable constraints (e.g., labeling) raises errors.
- `sum/3` and `scalar_product/4` are linear; `X*Y #= Z` with both unbound is non-linear and propagates weakly.
## Self-check
Count solutions of an `all_distinct` problem with `findall` after `label` and compare with `all_different`.
