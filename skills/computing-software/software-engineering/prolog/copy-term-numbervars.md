---
id: computing-software.software-engineering.prolog.copy-term-numbervars
name: copy-term-numbervars
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, copy-term-numbervars, term-variables]
level: practitioner
status: docs-checked
description: "Rename variables safely with copy_term/2, ground terms with numbervars/3, and list variables with term_variables/2."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=manual
  - https://www.metalevel.at/prolog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Copying and naming variables
```prolog
?- copy_term(f(X,Y,X), C).          % C = f(A,B,A): fresh variables, same sharing
?- T = g(X,Y), numbervars(T, 0, E), portray_clause(T).   % g(A, B). E=2
?- term_variables(f(X,g(Y,X)), Vs). % Vs = [X,Y]
?- copy_term([X], [Y], Gs).         % attributed vars: Gs holds residual goals
```
Use `copy_term/2` before asserting a term holding variables you still want to bind elsewhere.
## Gotchas
- `numbervars/3` unifies variables with `'$VAR'(N)` terms; `portray_clause/2` exploits the `numbervars` option to show letters.
- `copy_term/2` copies attributes (CLP(FD) constraints) too.
- `assert/1` stores a copy of the term, so variable bindings are not shared with the clause.
## Self-check
Verify `copy_term(X-Y-X, C)` keeps the sharing pattern using `C =@= X-Y-X`.

## Checked

2026-11-02. SWI-Prolog manual: copy_term/2 (fresh variables, attributes copied, ground sub-terms shared), copy_term/3 (attribute goals in Gs, Copy has no attributes), numbervars/3 ($VAR(N), End), term_variables/2, portray_clause using the numbervars option. Removed: the print/1 and write_canonical/1 comparison and the assert/1 copying line (not stated in the fetched sections).

Method: documentation only; no commands were run.
