---
id: computing-software.software-engineering.scheme-racket.case-lambda
name: case-lambda
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, case-lambda]
level: practitioner
status: docs-checked
description: "Overload a procedure by argument count with case-lambda; clauses are tried in order and no clause matching raises an arity error."
sources:
  - https://docs.racket-lang.org/guide/lambda.html
  - https://docs.racket-lang.org/guide/application.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# case-lambda dispatch on arity
**Goal:** arity-based dispatch.
```racket
(define area
  (case-lambda
    [(r) (* 3.14159 r r)]
    [(w h) (* w h)]))
```
- The first clause whose formals match the argument count is used, so put rest-argument clauses (`[args body ...]`) last.
- A `case-lambda` function cannot directly support optional or keyword arguments.
## Self-check
`(area 2)` and `(area 2 3)` work; `(area)` raises an arity error.

## Checked

Date: 2026-11-02. Confirmed on Racket Guide Arity-Sensitive Functions: case-lambda (first matching clause is applied; arity mismatch error; no direct optional or keyword arguments). Removed: the claim about when to prefer it over optional arguments, and the clause-order wording that the guide does not state.

Method: documentation only; no commands were run.
