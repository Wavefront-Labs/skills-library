---
id: computing-software.software-engineering.prolog.clpq-clpr
name: clpq-clpr
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, clpq-clpr, chr-rules]
level: advanced
status: draft
description: "Use library(clpq)/(clpr) linear constraints with {}/1 and write CHR rules (library(chr)) for custom solvers."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CLP(Q/R) and CHR
```prolog
:- use_module(library(clpq)).
?- {X = 2*Y + 1, Y = 3}.            % X = 7 (exact rationals)
?- {X >= 2, X =< 5}, sup(X, S), inf(X, I).   % S=5, I=2
:- use_module(library(chr)).
:- chr_constraint leq/2.
reflexivity  @ leq(X,X) <=> true.
antisymmetry @ leq(X,Y), leq(Y,X) <=> X = Y.
transitivity @ leq(X,Y), leq(Y,Z) ==> leq(X,Z).
```
- clpq uses exact rationals; clpr uses floats.
- CHR rule forms: simplification `<=>`, propagation `==>`, simpagation `\ ... <=>`.
## Gotchas
- Do not load clpq and clpr into the same module (operator/name clash).
- CHR rules run once at the constraint-add time; check the constraint store with `chr_show_store/1`.
## Self-check
Run the `leq` example: `leq(A,B), leq(B,A)` unifies A and B.
