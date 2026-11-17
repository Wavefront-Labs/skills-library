---
id: computing-software.software-engineering.prolog.aggregate-all
name: aggregate-all
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, aggregate-all, aggregate-library]
level: practitioner
status: docs-checked
description: "Count, sum, max, min and bag results with library(aggregate): aggregate_all(count/sum/max/bag) and foreach/2."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# library(aggregate)
```prolog
:- use_module(library(aggregate)).
?- aggregate_all(count, age(_, _), C).
?- aggregate_all(sum(A), age(_, A), S).
?- aggregate_all(max(A, N), age(N, A), max(MA, MN)).   % max with witness
?- aggregate_all(max(A), age(_, A), M).    % fails on an empty solution set
?- aggregate_all(bag(N), age(N, _), L).
?- foreach(member(X, [1,2,3]), dif(X, Y)).
```
## Gotchas
- `aggregate_all(max(X), ...)` fails with no solutions; `count` and `sum` give 0.
- `aggregate/3` (not `_all`) is built on `bagof/3`, so it groups on free variables and fails when there are no solutions.
- `count`, `sum`, `max` and `min` are computed incrementally in constant memory, so prefer `aggregate_all(count, ...)` over `findall` plus `length` for big result sets.
## Self-check
Compute average age with `aggregate_all(count/sum)` and guard division by zero.

## Checked

2026-11-02. library(aggregate) source and docs (swipl-devel library/aggregate.pl): templates count, sum(Expr), max(Expr), max(Expr, Witness) giving max(Max, Witness), bag(X); aggregate_all/3 fails for min/max on an empty set while count and sum give 0; incremental constant-memory processing; aggregate/3 uses bagof/3; foreach/2. Fixed: the max(A-N) example (max/1 takes a numeric expression; the witness form is max(Expr, Witness) returning max(Max, Witness)).

Method: documentation only; no commands were run.
