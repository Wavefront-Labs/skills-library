---
id: computing-software.software-engineering.prolog.accumulator-pattern
name: accumulator-pattern
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-accumulators, accumulator-pattern, accumulator-pair]
level: practitioner
status: draft
description: "Convert naive recursion into accumulator style, with worked reverse/3, sum and the Acc0/Acc argument pair convention."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Accumulator pattern
Naive `rev([H|T],R) :- rev(T,RT), append(RT,[H],R)` is O(n^2); with an accumulator it is O(n):
```prolog
rev(L, R) :- rev_(L, [], R).
rev_([], R, R).
rev_([H|T], A0, R) :- rev_(T, [H|A0], R).
sum(L, S) :- foldl([X,A0,A]>>(A is A0+X), L, 0, S).
```
Naming convention: `Acc0`/`Acc`, or `S0`/`S` (state threading); order of arguments: put the iteration data first for indexing.
## Gotchas
- Accumulator reverses output order for list builders.
- Keep the wrapper (`len/2`) separate from the worker (`len_/3`).
## Self-check
Implement `max_list` with an accumulator and compare to library `max_list/2`.
