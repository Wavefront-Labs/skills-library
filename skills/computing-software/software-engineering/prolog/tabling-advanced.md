---
id: computing-software.software-engineering.prolog.tabling-advanced
name: tabling-advanced
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, tabling-advanced, mode-directed-tabling]
level: advanced
status: docs-checked
description: "Use SWI-Prolog tabling modes (min, max, lattice), tnot/1 with well-founded semantics, and incremental tabling."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/man/tabling.plx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Advanced tabling
```prolog
:- table path(_,_,min).                 % answer subsumption: keep the minimum
:- table conn(_,lattice(shortest/3)).   % lattice(PI): PI is a predicate old,new,result
:- table (p/1, q/1) as incremental.
:- dynamic d/1 as incremental.
:- table p/0, q/0.
p :- tnot(q).
q :- tnot(p).                           % well-founded semantics: undefined
```
- Modes: index (`+`/plain argument), `-` or `first`, `last`, `min`, `max`, `sum`, `lattice(PI)`, `po(PI)`. `min` and `max` use the standard order of terms (numbers compare by value).
- `tnot/1` is tabled negation. Under well-founded semantics an answer can be `undefined`; the toplevel shows conditional answers as undefined.
- Incremental tabling: tables of predicates declared `as incremental` are invalidated by `assert` / `retract` on dynamic incremental predicates and re-evaluated lazily on the next access.
- Monotonic tabling also exists; it does not support negation.
## Gotchas
- Declare both the tabled predicate and the dynamic data it depends on as incremental; otherwise tables are not invalidated.
## Self-check
Query `p` in the example above; the answer is undefined, not true or false.

## Checked

2026-11-03. SWI-Prolog manual tabling chapter (tabling.plx in swipl-devel/man): answer subsumption modes, lattice/po, tnot/1 and WFS undefined answers, incremental tabling declarations and lazy re-evaluation (builtin.plx example `:- dynamic person/2 as incremental`), monotonic tabling remark. Removed: any claim about mixing incremental and non-incremental tables raising an error or warning.

Method: documentation only; no commands were run.
