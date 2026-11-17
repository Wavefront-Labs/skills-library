---
id: computing-software.software-engineering.scheme-racket.sicp-hierarchical-data
name: sicp-hierarchical-data
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sicp-hierarchical-data]
level: practitioner
status: draft
description: "Process list structure with map, filter, accumulate, flatmap and trees, and represent sets as lists or binary trees (SICP 2.2-2.3.3)."
sources:
  - https://sarabander.github.io/sicp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sequences, trees and sets
**Goal:** sequence-oriented programming.
```racket
(define (accumulate op init seq) (if (null? seq) init (op (car seq) (accumulate op init (cdr seq)))))
(define (flatmap f s) (accumulate append '() (map f s)))
(define (count-leaves t) (cond [(null? t) 0] [(pair? t) (+ (count-leaves (car t)) (count-leaves (cdr t)))] [else 1]))
```
- `accumulate` is `foldr`.
- Ordered-list and tree set representations give O(n) vs O(log n) membership.
## Self-check
`(count-leaves '((1 2) (3 (4))))` is `4`.
