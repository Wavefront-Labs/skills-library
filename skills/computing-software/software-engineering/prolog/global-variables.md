---
id: computing-software.software-engineering.prolog.global-variables
name: global-variables
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-global-state, global-variables, nb-setval]
level: advanced
status: docs-checked
description: "Use backtrackable b_setval/b_getval and non-backtrackable nb_setval/nb_getval global variables and flag/3 counters."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global variables
```prolog
?- nb_setval(counter, 0), forall(between(1,3,_), (nb_getval(counter,C), C1 is C+1, nb_setval(counter,C1))), nb_getval(counter, V).   % V = 3
?- b_setval(v, 1), b_getval(v, X).                 % undone on backtracking
?- flag(hits, Old, Old+1).                         % atomic update of a shared counter
```
- `nb_setval/2` stores a copy of the term; `nb_linkval/2` avoids the copy but its backtracking behaviour is poorly defined for compound terms (expert use only).
- Global variable values cannot be shared among threads; each thread has its own.
## Gotchas
- Prefer passing state through arguments or `foldl`; globals hide data flow and break purity.
- `nb_getval` of an unset key throws `existence_error(variable, Name)`.
## Self-check
Count solutions of a goal with `nb_setval` and `forall`, and compare with `aggregate_all(count, G, N)`.

## Checked

2026-11-02. SWI-Prolog manual global variables section: b_setval/2 (undone on backtracking), nb_setval/2 (copy via duplicate_term), nb_linkval/2 (no copy, poorly defined backtracking), nb_getval/2 (existence_error(variable, Name)), flag/3 (atomic, New may be an arithmetic expression), per-thread values.

Method: documentation only; no commands were run.
