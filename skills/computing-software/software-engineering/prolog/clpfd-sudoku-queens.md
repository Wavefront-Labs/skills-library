---
id: computing-software.software-engineering.prolog.clpfd-sudoku-queens
name: clpfd-sudoku-queens
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-clpfd-apps, clpfd-sudoku-queens, sudoku-puzzle]
level: practitioner
status: draft
description: "Model classic puzzles with CLP(FD): Sudoku with all_distinct rows and blocks, N-queens, and SEND+MORE."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Puzzle modelling pattern
Pattern: variables, domains, constraints, then label.
```prolog
puzzle([S,E,N,D] + [M,O,R,E] = [M,O,N,E,Y]) :-
    Vars = [S,E,N,D,M,O,R,Y], Vars ins 0..9, all_different(Vars),
    S*1000 + E*100 + N*10 + D + M*1000 + O*100 + R*10 + E #=
    M*10000 + O*1000 + N*100 + E*10 + Y,
    M #\= 0, S #\= 0.
?- puzzle(P), term_variables(P, Vs), label(Vs).
queens(N, Qs) :- length(Qs, N), Qs ins 1..N, safe(Qs), labeling([ff], Qs).
safe([]). safe([Q|Qs]) :- no_attack(Q, Qs, 1), safe(Qs).
no_attack(_, [], _).
no_attack(Q, [Q1|Qs], D) :- Q #\= Q1, abs(Q - Q1) #\= D, D1 is D+1, no_attack(Q, Qs, D1).
```
Sudoku: `maplist(all_distinct, Rows)`, transpose with `transpose/2` (clpfd), blocks of 3.
## Gotchas
- Always label after constraint posting; print solved variables, not the constraint store.
## Self-check
Solve 8-queens and verify with an independent checker; count all 92 solutions.
