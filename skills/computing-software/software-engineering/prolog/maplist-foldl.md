---
id: computing-software.software-engineering.prolog.maplist-foldl
name: maplist-foldl
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-higher-order, maplist-foldl, foldl-include]
level: practitioner
status: docs-checked
description: "Transform lists with maplist/2..N, foldl/4..6, include/3, exclude/3 and partition/4."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# library(apply)
```prolog
double(X, Y) :- Y is X * 2.
?- maplist(double, [1,2,3], L).          % [2,4,6]
?- maplist([X,Y,Z]>>(Z is X+Y), [1,2], [3,4], S).   % [4,6]
add(X, A0, A) :- A is A0 + X.
?- foldl(add, [1,2,3], 0, S).            % 6
?- partition([X]>>(X<3), [1,5,2], In, Out).
```
`maplist` itself is relational, but `double/2` above uses `is/2`, which evaluates its right operand and cannot be run backward; `maplist(double, L, [2,4])` therefore does not work.
## Gotchas
- `maplist/3` and friends apply `Goal` to matching elements of the lists (the source defines it element by element), so the lists must have the same length.
- The goal gets extra arguments appended: `maplist(foo(A), L)` calls `foo(A, E)`.
## Self-check
Compute the sum of squares of `[1,2,3]` with `maplist` and `foldl`.

## Checked

2026-11-02. library(apply) source: maplist/2..5 (call(G, X_1i, ..., X_mi) over matching elements), foldl/4..7, include/3, exclude/3, partition/4 (Included, Excluded), yall lambda library. Removed: the CLP(FD) advice.

Method: documentation only; no commands were run.
