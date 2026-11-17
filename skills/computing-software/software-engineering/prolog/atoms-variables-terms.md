---
id: computing-software.software-engineering.prolog.atoms-variables-terms
name: atoms-variables-terms
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-syntax, atoms-variables-terms, term-syntax]
level: intro
status: draft
description: "Read Prolog term syntax: atoms, quoted atoms, variables, anonymous _, compound terms and the period terminator."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Prolog term syntax
- Atom: starts lowercase (`foo`), symbol chars (`+`, `=..`), or quoted (`'Hello World'`).
- Variable: starts Uppercase or `_`; `_` alone is anonymous and never shares a binding.
- Compound: `f(a, X)`; functor name plus arity makes the predicate indicator `f/2`.
- A clause ends with `.` followed by whitespace or EOF. `foo:-bar.` fine; `X = 'a'.b` is not.
```prolog
parent(tom, bob).            % fact
grand(X, Z) :- parent(X, Y), parent(Y, Z).   % rule
?- X = point(1,2), X =.. L.  % L = [point,1,2]
```
## Gotchas
- `foo (a)` with a space is not a compound term call; no space between functor and `(`.
- Variables with the same name in one clause are the same variable; across clauses they are unrelated.
- `_Name` variables suppress singleton warnings but still share within a clause.
## Self-check
Predict, then run `?- X = f(_, _), copy_term(X, Y).` and confirm the two `_` are different variables.
