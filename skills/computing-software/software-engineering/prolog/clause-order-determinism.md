---
id: computing-software.software-engineering.prolog.clause-order-determinism
name: clause-order-determinism
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, clause-order-determinism, determinism]
level: practitioner
status: draft
description: "Make predicates deterministic with first-argument indexing, mutually exclusive clauses and det checks without needless cuts."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Determinism and clause order
Goal: a predicate that leaves no choice point on its intended mode.
- Make clause heads mutually exclusive on the first argument so indexing avoids a choice point.
- Check with `?- call_cleanup(Goal, Det=true).` or watch for the toplevel `;` prompt.
- SWI-Prolog 9 has `$/1` and `$/0` determinism declarations (version unconfirmed).
```prolog
last([X], X).          % leaves a choice point on [_|_]: both clauses can match
last([_|T], X) :- T = [_|_], last(T, X).   % exclusive form
```
## Gotchas
- Indexing is on the first argument by default; JIT indexing may pick other args.
- Replace `!` by a guard (`T = [_|_]`) or `dif/2` to keep the predicate relational.
## Self-check
Query your predicate at the toplevel: it must end with `.` and not wait at `;`.
