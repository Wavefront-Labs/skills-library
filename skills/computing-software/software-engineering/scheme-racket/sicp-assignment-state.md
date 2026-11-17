---
id: computing-software.software-engineering.scheme-racket.sicp-assignment-state
name: sicp-assignment-state
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sicp-assignment-state, sicp-state]
level: intro
status: draft
description: "Model objects with closures and set!, such as make-account and make-counter with message passing (SICP 3.1)."
sources:
  - https://sarabander.github.io/sicp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Assignment and local state
**Goal:** state via closures.
```racket
(define (make-account balance)
  (define (withdraw a) (if (>= balance a) (begin (set! balance (- balance a)) balance) "Insufficient funds"))
  (define (dispatch m) (cond [(eq? m 'withdraw) withdraw] [else (error "unknown" m)]))
  dispatch)
((( make-account 100) 'withdraw) 30)
```
- Assignment breaks substitution model reasoning; two calls of the same expression can differ.
## Self-check
Two accounts do not share balance.
