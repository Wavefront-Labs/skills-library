---
id: computing-software.software-engineering.prolog.tabling-basics
name: tabling-basics
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-tabling, tabling-basics, table-directive]
level: practitioner
status: docs-checked
description: "Memoise and fix left-recursive predicates with :- table, understand completion and variant checking."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tabling basics
```prolog
:- table path/2.
edge(a,b). edge(b,c). edge(c,a).
path(X,Y) :- path(X,Z), edge(Z,Y).    % left-recursive, terminates when tabled
path(X,Y) :- edge(X,Y).
?- path(a, X).
:- table fib/2.
fib(0,0). fib(1,1).
fib(N,F) :- N>1, A is N-1, B is N-2, fib(A,FA), fib(B,FB), F is FA+FB.
?- fib(200, F).
```
- `abolish_all_tables/0` removes all tables; incremental tabling needs both the tabled predicate (`:- table p/1 as incremental`) and the dynamic predicate (`:- dynamic([d/1], [incremental(true)])`) to have the `incremental` property.
- Answers are memoized in answer tries.
## Gotchas
- The manual says tabling is intended for programs without side effects or pruning of choice points (cut, `->`).
- Table memory is limited by the table space (`--table-space` command-line option, default 1Gb on 64-bit machines); `abolish_all_tables/0` frees it.
## Self-check
Run the cyclic graph `path(a,X)`; it must terminate with 3 answers.

## Checked

2026-11-02. SWI-Prolog manual chapter on tabling: table/1 directive, abolish_all_tables/0, incremental tabling (table ... as incremental, dynamic/2 incremental(true)), answer tries, intended for programs without side effects or pruning, --table-space option default. Removed: the set_prolog_flag(table_space) form and the per-call-variant statement.

Method: documentation only; no commands were run.
