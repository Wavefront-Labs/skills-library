---
id: computing-software.software-engineering.prolog.sort-msort-predsort
name: sort-msort-predsort
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, sort-msort-predsort, sort-4]
level: practitioner
status: docs-checked
description: "Sort with sort/2, sort/4 on a key with ordering and duplicates, msort/2, predsort/3 and stable keysort/2."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sorting
```prolog
?- sort(0, @>=, [3,1,2,3], L).          % L = [3,3,2,1] descending, keep duplicates
?- sort(1, @<, [f(2,a),f(1,b)], L).     % sort on 1st argument: [f(1,b),f(2,a)]
?- msort([b,a,b], L).                   % [a,b,b] keeps duplicates
?- keysort([2-b,1-a,2-a], L).           % stable: [1-a,2-b,2-a]
cmp(O, A-_, B-_) :- compare(O, A, B).
?- predsort(cmp, [2-x,1-y,2-z], L).     % removes elements where O is (=)
```
## Gotchas
- `sort/4` Order: `@<` ascending, remove duplicates; `@=<` ascending, keep; `@>` descending, remove; `@>=` descending, keep. The sort is stable. Key 0 sorts on the whole term, N sorts on the N-th argument.
- `predsort/3` calls `Pred(-Delta, +E1, +E2)` with Delta one of `<`, `>`, `=`; an `=` result collapses the two elements into one, so return `<` or `>` to keep both.
- `sort/2` sorts by the standard order of terms and removes duplicates (natural merge sort in C); it can sort a cyclic list. `msort/2` is the same without removing duplicates.
## Self-check
Sort a list of `person(Name,Age)` by Age descending using `sort/4`.

## Checked

2026-11-02. SWI-Prolog manual sorting entries: sort/2 (standard order, duplicates removed, natural merge sort), sort/4 (Key 0 or argument index, Order table @< @=< @> @>=, stable), msort/2, keysort/2 (stable, keeps duplicates), predsort/3 (Delta in <, >, =; = collapses). Removed: the O(n log n) figure.

Method: documentation only; no commands were run.
