---
id: computing-software.software-engineering.prolog.unification-occurs-check
name: unification-occurs-check
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-unification, unification-occurs-check, occurs-check]
level: practitioner
status: docs-checked
description: "Handle cyclic terms in SWI-Prolog: unify_with_occurs_check/2, the occurs_check flag, cyclic_term/1 and write_term cycles."
sources:
  - https://www.swi-prolog.org/pldoc/man?predicate=unify_with_occurs_check/2
  - https://www.swi-prolog.org/pldoc/man?predicate=write_term/2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Occurs check
```prolog
?- X = f(X).                            % succeeds: creates a rational tree
?- unify_with_occurs_check(X, f(X)).    % fails
?- set_prolog_flag(occurs_check, error).
?- cyclic_term(T), acyclic_term(U).
?- \+ a = b.                            % T1 \= T2 is equivalent to \+ T1 = T2
```
- `=/2` does no occurs check by default, so `X = f(X)` makes a cyclic term.
- `unify_with_occurs_check/2` is the ISO predicate; it fails on cycle creation and is safe with cyclic terms. It only guards the creation of cycles.
- Flag `occurs_check`: `false` (default), `true` (unification that would create a cycle fails silently), `error` (raises an `occurs_check` exception). The flag is global and may break libraries.
- `cyclic_term/1` and `acyclic_term/1` test terms.
- `write_term/2` option `cycles(Bool)` defaults to true and prints cyclic terms as `@(Template, Substitutions)`; with `cycles(false)` and no `max_depth` a cyclic term raises a domain error.
## Gotchas
- Setting the flag globally changes the behaviour of every library.
## Self-check
`X = f(X), cyclic_term(X)` succeeds; `unify_with_occurs_check(X, f(X))` fails.

## Checked

2026-11-03. SWI-Prolog manual: =/2, unify_with_occurs_check/2, flag occurs_check (false, true, error), cyclic_term/1, acyclic_term/1, `\=/2`, write_term/2 cycles option. Removed: the `\==` remark and the claim that writing a cyclic term loops (the default `cycles(true)` prints it with `@/2`).

Method: documentation only; no commands were run.
