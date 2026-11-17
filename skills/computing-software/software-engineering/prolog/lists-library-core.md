---
id: computing-software.software-engineering.prolog.lists-library-core
name: lists-library-core
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-lists-library, lists-library-core, append-member]
level: intro
status: docs-checked
description: "Use the core list predicates: append/3, member/2, memberchk/2, nth0/nth1, reverse/2, last/2, sum_list/2, max_list/2."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# library(lists) core
```prolog
?- append(X, Y, [1,2]).            % enumerates all splits
?- member(X, [a,b,c]).             % nondeterministic
?- memberchk(b, [a,b,c]).          % deterministic, first match only
?- nth1(2, [a,b,c], X).            % X = b ; nth0 is zero-based
?- reverse([1,2,3], R), sum_list(R, S), max_list(R, M).
?- exclude([X]>>(X>1), [1,2,3], L).    % L = [1]
?- subtract([a,b,c], [b], L).      % L = [a,c]
```
## Gotchas
- `memberchk/2` is semidet (first match only, builtin); `member/2` is nondeterministic and leaves a choice point.
- `reverse/2` is deterministic if either list is a proper list; if both are partial lists, backtracking generates increasingly long lists.
- `delete/3` removes elements that unify with the given one and is deprecated in the library docs; `exclude/3` (library(apply)) is the general filter.
## Self-check
Enumerate `append(X, [c], [a,b,c])` and confirm one solution.

## Checked

2026-11-02. library(lists) and library(apply) sources plus manual: append/3 (enumerates splits), memberchk/2 (semidet builtin), nth0/3 and nth1/3, reverse/2 (determinism note), sum_list/2, max_list/2, subtract/3 (unification via memberchk/2), delete/3 (deprecated, unifying elements), exclude/3.

Method: documentation only; no commands were run.
