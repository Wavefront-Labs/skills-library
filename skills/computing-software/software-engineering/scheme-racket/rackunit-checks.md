---
id: computing-software.software-engineering.scheme-racket.rackunit-checks
name: rackunit-checks
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, rackunit-checks]
level: intro
status: docs-checked
description: "RackUnit check forms: check-equal?, check-=, check-exn (takes a thunk), check-true; failure reports show name, location, actual and expected."
sources:
  - https://docs.racket-lang.org/rackunit/api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# check forms
**Goal:** write assertions.
```racket
(require rackunit)
(check-equal? (+ 1 1) 2 "adds")
(check-= 0.1 (/ 1 10.0) 1e-9)
(check-exn exn:fail? (lambda () (error "x")))
(check-true (even? 2))
```
- `(check-= v1 v2 epsilon [message])` passes when the numbers are within `epsilon`; the optional message appears if the check fails.
- `check-exn` takes `exn-predicate` and a thunk (a function of no arguments), not an expression. The manual calls passing an expression instead of a thunk a common error.
- Checks are conceptually functions: arguments are evaluated once before the check body runs, so code to be tested for exceptions must be wrapped in a thunk.
- A failure report prints the check name, location and, for `check-equal?`, the actual and expected values.
- Inside `test-begin` or `test-case`, a failing expression stops the rest of that group.
## Self-check
Make a check fail and read the printed `FAILURE` report with `actual` and `expected`.
## Checked
2026-11-08. Confirmed on the RackUnit API page: signatures and semantics of `check-=`, `check-exn`, `check-true`, the thunk rule, and failure output examples; and the `test-begin`/`test-case` short-circuit text. Removed: "checks do not stop the file unless in a test-case" (not stated on the page).
Method: documentation only; no commands were run.
