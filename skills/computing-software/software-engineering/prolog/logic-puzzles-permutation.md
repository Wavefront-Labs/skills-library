---
id: computing-software.software-engineering.prolog.logic-puzzles-permutation
name: logic-puzzles-permutation
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, logic-puzzles-permutation, zebra-puzzle]
level: practitioner
status: draft
description: "Solve zebra-style puzzles with member/select/permutation, constraints placed early and verify uniqueness."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Logic puzzles
```prolog
right_of(A, B, [B,A|_]).
right_of(A, B, [_|T]) :- right_of(A, B, T).
next_to(A, B, L) :- right_of(A, B, L) ; right_of(B, A, L).
zebra(Owner) :-   % fragment: add the remaining clues
    Hs = [h(_,norwegian,_,_,_),_,h(_,_,_,milk,_),_,_],
    member(h(red,english,_,_,_), Hs),
    member(h(green,_,_,coffee,_), Hs),
    right_of(h(green,_,_,_,_), h(ivory,_,_,_,_), Hs),
    member(h(_,Owner,zebra,_,_), Hs).
?- zebra(O).
```
Order constraints so that the most restrictive come first; or use CLP(FD) with all_different.
## Gotchas
- Generate-and-test with `permutation/2` explodes: check partial constraints early.
- Verify the solution is unique with `findall` and `length`.
## Self-check
Count solutions with `aggregate_all(count, zebra(_), N)` (expect 1 for a well-formed puzzle).
