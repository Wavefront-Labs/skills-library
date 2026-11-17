---
id: computing-software.software-engineering.prolog.facts-rules-queries
name: facts-rules-queries
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-modelling, facts-rules-queries, family-tree]
level: intro
status: draft
description: "Model a domain with facts and recursive rules (family tree, ancestors) and query it in several modes."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Facts and rules
```prolog
parent(tom, bob). parent(bob, ann). parent(bob, pat).
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
sibling(X, Y) :- parent(P, X), parent(P, Y), dif(X, Y).
?- ancestor(tom, Who).        % enumerate descendants
?- ancestor(Who, ann).        % enumerate ancestors
?- sibling(ann, S).
```
- Use one relation in many modes: input/output roles are not fixed.
- Name relations descriptively (`parent_child/2`) and keep arguments consistent.
## Gotchas
- Ancestor with left recursion `ancestor(X,Y) :- ancestor(X,Z), parent(Z,Y)` loops.
- `sibling` without `dif/2` returns X as its own sibling.
## Self-check
Add `cousin/2`, query both directions, and confirm no self-cousins.
