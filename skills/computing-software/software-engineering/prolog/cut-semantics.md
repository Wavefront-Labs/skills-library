---
id: computing-software.software-engineering.prolog.cut-semantics
name: cut-semantics
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-cut, cut-semantics, green-red-cut]
level: practitioner
status: draft
description: "Use ! correctly: commit to a clause, distinguish green from red cuts and know its scope in call/1 and ->."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cut
`!` discards choice points created since the parent goal was called (including remaining clauses).
```prolog
max(X, Y, X) :- X >= Y, !.
max(_, Y, Y).              % max(3,1,1) wrongly succeeds via clause 2
max2(X, Y, Z) :- ( X >= Y -> Z = X ; Z = Y ).   % prefer if-then-else
```
- Green cut: only removes redundant solutions. Red cut: changes meaning.
- Cut inside `call((G, !))` is local to the call.
## Gotchas
- Keep output unification after the cut, or the predicate breaks when called with bound outputs.
- Cut in `\+`, an `->` condition, and `findall` goals is local.
## Self-check
Query `max(3, 1, 1)` against the first definition and explain the wrong answer.
