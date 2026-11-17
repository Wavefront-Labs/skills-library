---
id: computing-software.software-engineering.scheme-racket.define-values
name: define-values
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, define-values]
level: practitioner
status: docs-checked
description: "Return and bind several values with values, define-values, let-values and call-with-values; mismatched counts raise errors."
sources:
  - https://docs.racket-lang.org/guide/define.html
  - https://docs.racket-lang.org/reference/define.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple values with define-values
**Goal:** use multiple return values.
```racket
(define (min-max l) (values (apply min l) (apply max l)))
(define-values (lo hi) (min-max '(3 1 4)))
(call-with-values (lambda () (values 1 2)) +)  ; => 3
```
- The number of results produced by the expression must match the number of identifiers.
- A `define` that is not the function shorthand is equivalent to `define-values` with a single identifier.
## Self-check
`(define-values (a b) (values 1))` raises a result-arity mismatch.

## Checked

Date: 2026-11-02. Confirmed on Racket Guide Multiple Values and define-values (result count must match; `define` equals single-identifier `define-values`) and the Reference for `call-with-values`. Removed: the `(+ (values 1 2) 1)` and `(values x)` bullets.

Method: documentation only; no commands were run.
