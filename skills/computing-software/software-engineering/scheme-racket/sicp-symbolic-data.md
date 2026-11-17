---
id: computing-software.software-engineering.scheme-racket.sicp-symbolic-data
name: sicp-symbolic-data
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sicp-symbolic-data]
level: practitioner
status: draft
description: "Differentiate algebraic expressions with symbols, quote, constructors and simplifying make-sum / make-product (SICP 2.3)."
sources:
  - https://sarabander.github.io/sicp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Symbolic data: differentiation
**Goal:** symbolic manipulation.
```racket
(define (deriv e v)
  (cond [(number? e) 0]
        [(symbol? e) (if (eq? e v) 1 0)]
        [(eq? (car e) '+) (list '+ (deriv (cadr e) v) (deriv (caddr e) v))]
        [(eq? (car e) '*) (list '+ (list '* (cadr e) (deriv (caddr e) v)) (list '* (deriv (cadr e) v) (caddr e)))]))
```
- Without simplification results balloon; add `make-sum` that folds numeric zero and one.
- Racket `match` shortens this considerably.
## Self-check
`(deriv '(* x x) 'x)` before and after simplification.
