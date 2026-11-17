---
id: computing-software.software-engineering.prolog.list-structure
name: list-structure
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-datatypes, list-structure, list-head-tail]
level: intro
status: draft
description: "Understand lists as nested head-tail cells ending in the empty list, and write recursive predicates over them."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lists and [H|T]
A list is `[a,b,c] = [a|[b|[c|[]]]]`. In SWI-Prolog 7+ the cell functor is `'[|]'`, and `[]` is a reserved constant distinct from the atom `'[]'`.
```prolog
len([], 0).
len([_|T], N) :- len(T, M), N is M + 1.
?- [H|T] = [1,2,3].   % H=1, T=[2,3]
?- length(L, 2).      % L = [_A,_B]
```
## Gotchas
- `[a|b]` is a partial (improper) list; `is_list/1` fails on it.
- `length/2` with unbound list enumerates on backtracking: guard against infinite loops.
- Always put the base case before the recursive clause and keep them mutually exclusive.
## Self-check
Run `?- length(L, N).` and take three solutions; explain why the list lengths grow.
