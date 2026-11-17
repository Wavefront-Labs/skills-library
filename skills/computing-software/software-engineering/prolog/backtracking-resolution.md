---
id: computing-software.software-engineering.prolog.backtracking-resolution
name: backtracking-resolution
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-execution, backtracking-resolution, choice-points]
level: intro
status: draft
description: "Trace how Prolog resolves goals top-down, left-to-right, creating choice points and backtracking on failure."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backtracking and choice points
Prolog selects the leftmost goal, tries clauses in textual order, and on failure retreats to the most recent choice point.
```prolog
colour(red). colour(green). colour(blue).
?- colour(X), X \== red.     % X = green ; X = blue.
?- forall(colour(C), (write(C), nl)).
```
Use `;` at the toplevel to ask for more answers. A predicate leaves a choice point when clauses remain that might match.
## Gotchas
- Side effects (write, assert) are not undone on backtracking.
- Order of goals changes termination, not logic: put cheap, selective goals first.
- Left recursion `p :- p, q.` loops; fix by reordering or tabling.
## Self-check
Predict the order of solutions for `?- member(X,[a,b]), member(Y,[1,2]).` and verify.
