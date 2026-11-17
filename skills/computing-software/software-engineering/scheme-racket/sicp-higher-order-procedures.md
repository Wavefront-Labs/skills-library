---
id: computing-software.software-engineering.scheme-racket.sicp-higher-order-procedures
name: sicp-higher-order-procedures
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sicp-higher-order-procedures]
level: practitioner
status: draft
description: "Abstract patterns with sum, fixed-point, average-damp and procedures returning procedures (SICP 1.3)."
sources:
  - https://sarabander.github.io/sicp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Higher-order procedures
**Goal:** pass and return procedures.
```racket
(define (sum term a next b) (if (> a b) 0 (+ (term a) (sum term (next a) next b))))
(define (fixed-point f guess) (let ([n (f guess)]) (if (< (abs (- n guess)) 1e-9) n (fixed-point f n))))
(fixed-point cos 1.0)
```
- Racket's `foldl`, `compose`, `curry` express the same ideas.
## Self-check
`(sum (lambda (x) x) 1 add1 10)` is `55`.
