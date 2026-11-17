---
id: computing-software.software-engineering.scheme-racket.rest-arguments
name: rest-arguments
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, rest-arguments]
level: intro
status: docs-checked
description: "Accept variable arguments with a dotted parameter or (define (f . args)), and spread lists into calls with apply."
sources:
  - https://docs.racket-lang.org/guide/lambda.html
  - https://docs.racket-lang.org/guide/apply.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rest arguments and apply
**Goal:** variadic functions.
```racket
(define (sum . xs) (apply + xs))
(define (f a . more) (list a more))
(apply f 1 '(2 3))  ; => '(1 (2 3))
```
- `apply` accepts additional arguments between the function and the list; they are consed onto the list.
- Keyword arguments can be combined with a rest argument in the formals: `(define (g #:k [k 0] . xs) ...)`.
- Keywords inside the list given to `apply` are treated as positional arguments; use `keyword-apply` to pass keywords from a list.
## Self-check
`(sum)` returns `0`; `(apply sum '(1 2 3))` returns `6`.

## Checked

Date: 2026-11-02. Confirmed on Racket Guide Functions: lambda (rest arguments, rest with required arguments, keyword and rest formals) and The apply Function. Fixed sources (apply.html replaces application.html). Added: the keywords-in-apply-list caveat.

Method: documentation only; no commands were run.
