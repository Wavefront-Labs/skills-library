---
id: computing-software.software-engineering.prolog.vanilla-meta-interpreter
name: vanilla-meta-interpreter
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-meta, vanilla-meta-interpreter, solve-clause]
level: advanced
status: draft
description: "Write solve/1 using clause/2, extend it for depth limits, proof trees and tracing."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Meta-interpreters
```prolog
:- dynamic app/3.
solve(true) :- !.
solve((A,B)) :- !, solve(A), solve(B).
solve(H) :- predicate_property(H, built_in), !, call(H).
solve(H) :- clause(H, Body), solve(Body).
% depth-limited
solve(true, _) :- !.
solve((A,B), D) :- !, solve(A, D), solve(B, D).
solve(H, D) :- D > 0, D1 is D-1, clause(H, B), solve(B, D1).
```
Extend to build proof trees: `solve(H, node(H, Subs))`.
## Gotchas
- `clause/2` works only on dynamic predicates or when `protect_static_code` is false.
- Handle control constructs (`;`, `->`, `\+`) explicitly.
- A meta-interpreter is much slower than direct execution.
## Self-check
Run `solve(app([1],[2],X))` on a dynamic `app/3` and print a proof tree.
