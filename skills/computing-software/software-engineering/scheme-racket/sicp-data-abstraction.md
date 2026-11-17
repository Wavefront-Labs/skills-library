---
id: computing-software.software-engineering.scheme-racket.sicp-data-abstraction
name: sicp-data-abstraction
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sicp-data-abstraction, sicp-data]
level: intro
status: draft
description: "Define constructors and selectors (make-rat, numer, denom) and abstraction barriers as in SICP 2.1."
sources:
  - https://sarabander.github.io/sicp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data abstraction with rational numbers
**Goal:** separate representation from use.
```racket
(define (make-rat n d) (let ([g (gcd n d)]) (cons (/ n g) (/ d g))))
(define numer car) (define denom cdr)
(define (add-rat a b) (make-rat (+ (* (numer a) (denom b)) (* (numer b) (denom a))) (* (denom a) (denom b))))
```
- Racket has built-in exact rationals; the exercise is the barrier, not the arithmetic.
## Self-check
Change representation to a struct without altering `add-rat`.
