---
id: computing-software.software-engineering.scheme-racket.r7rs-guard
name: r7rs-guard
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, r7rs-guard, r7rs-small]
level: practitioner
status: docs-checked
description: "R7RS-small guard, raise, raise-continuable, error and error-object accessors for portable exception handling."
sources:
  - https://small.r7rs.org/attachment/r7rs.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# R7RS guard, raise and error objects
**Goal:** portable exception handling.
```scheme
(guard (e ((string? e) (list 'str e))
          ((error-object? e) (error-object-message e)))
  (raise "oops"))
```
- `(guard (variable cond-clause ...) body ...)` evaluates the body with an exception handler that binds the raised object to the variable, then evaluates the clauses as the clauses of a `cond`.
- If no clause's test is true and there is no `else`, `raise-continuable` is invoked on the raised object in the dynamic environment of the original `raise` or `raise-continuable`.
- `(raise obj)` can raise any object. `(error message obj ...)` raises a new implementation-defined object that satisfies `error-object?`; `error-object-message` and `error-object-irritants` read it back.
- If a handler returns from `raise`, a secondary exception is raised; with `raise-continuable` the handler's values become the result.
## Self-check
`(guard (e (#t 'caught)) (error "x"))` returns `caught`.
## Checked
2026-11-08. Confirmed in the R7RS-small report, sections 4.2.7 (Exception handling) and 6.11 (Exceptions): `guard` semantics, `raise`, `raise-continuable`, `error`, `error-object?`, `error-object-message`, `error-object-irritants`. Removed: the Racket mapping claims ("Racket maps these onto its exceptions") because the Racket r7rs page was not readable.
Method: documentation only; no commands were run.
