---
id: computing-software.software-engineering.prolog.search-astar
name: search-astar
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, search-astar, heaps-priority-queue]
level: advanced
status: draft
description: "Implement best-first or A* search with a priority queue (library(heaps)) and admissible heuristics."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# A* search
```prolog
:- use_module(library(heaps)).
astar(Start, Goal, Path, Cost) :-
    h(Start, H0), list_to_heap([H0-node(Start,[Start],0)], Open),
    astar_(Open, [], Goal, Path, Cost).
astar_(Open, Closed, Goal, Path, Cost) :-
    get_from_heap(Open, _, node(N,Rev,G), Rest),
    (   N == Goal -> reverse(Rev, Path), Cost = G
    ;   \+ memberchk(N, Closed),
        findall(F-node(M,[M|Rev],G1), (edge(N,M,C), G1 is G+C, h(M,H), F is G1+H), Ns),
        foldl([K-V,H0,H1]>>add_to_heap(H0,K,V,H1), Ns, Rest, Open1),
        astar_(Open1, [N|Closed], Goal, Path, Cost)
    ;   astar_(Rest, Closed, Goal, Path, Cost) ).
```
Heap API: `empty_heap/1`, `add_to_heap/4`, `get_from_heap/4`, `list_to_heap/2`.
## Gotchas
- The heuristic must be admissible (never overestimates) for optimal paths.
- The closed list as a list is O(n): use rbtrees for big graphs.
- When the code above hits a closed node the third branch skips it (the `;` ordering).
## Self-check
Run on a weighted graph where the greedy path is not shortest and compare.
