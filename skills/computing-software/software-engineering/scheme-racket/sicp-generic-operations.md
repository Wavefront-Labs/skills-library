---
id: computing-software.software-engineering.scheme-racket.sicp-generic-operations
name: sicp-generic-operations
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sicp-generic-operations]
level: advanced
status: draft
description: "Dispatch on type tags with an operation table (put/get) to build generic arithmetic, as in SICP 2.4-2.5."
sources:
  - https://sarabander.github.io/sicp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generic operations and data-directed programming
**Goal:** extensible dispatch.
```racket
(define table (make-hash))
(define (put op type proc) (hash-set! table (list op type) proc))
(define (get op type) (hash-ref table (list op type) #f))
(define (attach-tag t c) (cons t c))
(define (apply-generic op x) ((get op (car x)) (cdr x)))
```
- Racket `racket/generic` or struct methods cover the same need natively.
- Coercion adds a towers-of-types design problem.
## Self-check
Register `area` for 'circle and 'rect and dispatch.
