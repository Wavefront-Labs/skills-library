---
id: computing-software.software-engineering.prolog.difference-lists
name: difference-lists
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, difference-lists, dlist-append]
level: advanced
status: draft
description: "Append in O(1) with difference lists List-Tail pairs, the DList pattern and relation to DCG translation."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Difference lists
Represent a list as `Xs-Ys`: the list is `Xs` with its tail `Ys` open.
```prolog
dl_append(A-B, B-C, A-C).
?- dl_append([1,2|T]-T, [3|U]-U, R).     % R = [1,2,3|U]-U
queue_empty(Q-Q).
enqueue(X, Q-[X|T], Q-T).
```
DCG translation uses the same idea with two extra arguments.
## Gotchas
- The open tail must remain unbound until closed with `[]`.
- Destructive unification: reuse of the same difference list twice yields wrong results.
- Do not use `==` on partial lists.
## Self-check
Build a list of 1..N in a single left-to-right pass using a difference list and close it with `T = []`.
