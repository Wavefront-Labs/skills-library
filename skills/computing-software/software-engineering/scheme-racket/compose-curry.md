---
id: computing-software.software-engineering.scheme-racket.compose-curry
name: compose-curry
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, compose-curry]
level: practitioner
status: docs-checked
description: "Build procedures with compose, curry, curryr, const, negate and thunk from racket/function."
sources:
  - https://docs.racket-lang.org/reference/procedures.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# compose, curry and procedure combinators
**Goal:** point-free helpers.
```racket
(require racket/function)
((compose add1 *) 2 3)     ; 7, right to left
((curry + 1) 2)            ; 3
(filter (negate zero?) '(0 1 2))
```
- `compose` applies the last procedure first and the first procedure last; `compose1` restricts passing between functions to a single value.
- `(curry proc v ...)` is equivalent to `((curry proc) v ...)`; the curried procedure accumulates arguments until the number acceptable under `procedure-arity` is reached, then calls `proc`.
## Self-check
`((compose list add1) 1)` returns `'(2)`.

## Checked

Date: 2026-11-02. Confirmed on Racket Reference Procedures (`compose`, `compose1`, `curry` in the Additional Higher-Order Functions section, which is `racket/function`; `negate`). Fixed sources (the earlier ones were the for and pairs pages). Removed: the varargs-curry advice.

Method: documentation only; no commands were run.
