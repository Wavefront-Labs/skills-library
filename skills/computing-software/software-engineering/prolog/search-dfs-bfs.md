---
id: computing-software.software-engineering.prolog.search-dfs-bfs
name: search-dfs-bfs
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-search, search-dfs-bfs, iterative-deepening]
level: practitioner
status: draft
description: "Implement graph search in Prolog: DFS with visited lists, BFS with queues and iterative deepening with length/2."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Graph search
```prolog
edge(a,b). edge(b,c). edge(c,d). edge(a,d).
path(S, G, P) :- dfs(S, G, [S], R), reverse(R, P).
dfs(G, G, V, V).
dfs(S, G, V, P) :- edge(S, N), \+ memberchk(N, V), dfs(N, G, [N|V], P).
% iterative deepening
idpath(S, G, P) :- length(P, _), P = [S|_], chain(P, G).
bfs(S, G, P) :- bfs_([[S]], G, R), reverse(R, P).
bfs_([[G|T]|_], G, [G|T]).
bfs_([[N|T]|Q], G, P) :- findall([M,N|T], (edge(N,M), \+ memberchk(M,[N|T])), Ns), append(Q, Ns, Q2), bfs_(Q2, G, P).
```
- DFS uses the Prolog stack; for cyclic graphs track visited nodes or use tabling.
- `length(P, _)` yields iterative deepening naturally.
## Gotchas
- `append(Q, Ns, Q2)` is O(n); use a difference list for large queues.
- Visited check via list is O(n); use `library(assoc)` or ordsets.
## Self-check
Find a shortest path with BFS and compare to the DFS result on a graph with a cycle.
