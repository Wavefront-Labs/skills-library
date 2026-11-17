---
id: computing-software.software-engineering.prolog.assert-retract
name: assert-retract
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-database, assert-retract, assertz-retract]
level: practitioner
status: docs-checked
description: "Modify the clause database with assertz/1, asserta/1, retract/1, retractall/1 and understand the logical update view."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# assert and retract
```prolog
:- dynamic counter/1, fact/2.
counter(0).
inc :- retract(counter(N)), N1 is N+1, assertz(counter(N1)).
?- retractall(fact(_, _)).      % succeeds even if none
?- asserta(fact(a, 1)), assertz(fact(b, 2)).
```
- `asserta/1` adds first, `assertz/1` last.
- `retract/1` is nondeterministic: it removes the first matching clause, more on backtracking.
## Gotchas
- `retractall/1` on an undefined predicate creates it as dynamic; declare `:- dynamic` for predicates you assert into.
- Logical update view: a running iteration over a predicate does not see clauses added meanwhile.
- Guard assert-based shared state with `with_mutex/2` (it runs the goal as `once/1` while holding the mutex); or pass state explicitly, or use `nb_setval/2`.
## Self-check
Implement a counter that survives backtracking, and show the retract/assert pair is atomic only within a mutex.

## Checked

2026-11-02. SWI-Prolog manual: retract/1 (first unifying clause, nondeterministic, logical update view with the insect/bee example), retractall/1 (succeeds, creates a dynamic predicate if undefined), asserta/assertz ordering, with_mutex/2, nb_setval/2. Removed: the unsupported claim that undeclared predicates always throw existence_error and the blanket thread-safety claim.

Method: documentation only; no commands were run.
