---
id: computing-software.software-engineering.prolog.findall-bagof-setof
name: findall-bagof-setof
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-all-solutions, findall-bagof-setof, caret-existential]
level: practitioner
status: docs-checked
description: "Collect solutions with findall/3, group them with bagof/3 and setof/3 using ^, and know the empty-result difference."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# findall, bagof, setof
```prolog
age(peter, 7). age(ann, 11). age(pat, 8). age(tom, 5). age(mike, 11).
?- findall(N, age(N, _), L).            % all names; L = [] if none
?- setof(N-A, age(N, A), L).            % sorted unique; fails if none
?- bagof(N, age(N, A), L).              % groups by free variable A, backtracks
?- bagof(N, A^age(N, A), L).            % ^ existentially quantifies A: one list
?- findall(N, age(N, 11), L, Tail).     % findall/4 difference list
```
## Gotchas
- `bagof/setof` fail with no solutions; `findall` returns `[]`.
- Free variables in the goal make `bagof/3` and `setof/3` backtrack over their alternatives; `Var^Goal` tells them not to bind `Var`.
## Self-check
Predict `bagof(N, age(N, A), L)` solutions and run it.

## Checked

2026-11-02. SWI-Prolog manual: findall/3 and findall/4 (difference list Bag-Tail), bagof/3 (backtracks over free variables, Var^Goal, fails if no solutions), setof/3 (as bagof/3 but sorted without duplicates). Removed: the findall result-copying note.

Method: documentation only; no commands were run.
