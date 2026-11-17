---
id: computing-software.software-engineering.scheme-racket.sicp-metacircular-evaluator
name: sicp-metacircular-evaluator
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sicp-metacircular-evaluator, sicp-evaluators]
level: advanced
status: draft
description: "Write eval and apply for a Scheme subset in Scheme: environments, special forms, primitive procedures, REPL driver (SICP 4.1)."
sources:
  - https://sarabander.github.io/sicp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Metacircular evaluator
**Goal:** understand language implementation.
```racket
(define (m-eval e env)
  (cond [(number? e) e]
        [(symbol? e) (lookup e env)]
        [(eq? (car e) 'quote) (cadr e)]
        [(eq? (car e) 'lambda) (list 'proc (cadr e) (cddr e) env)]
        [else (m-apply (m-eval (car e) env) (map (lambda (x) (m-eval x env)) (cdr e)))]))
```
- Needs `lookup`, `extend-environment`, `m-apply`; the SICP book lists them.
- Tail-call behaviour of the host determines tail calls in the guest.
## Self-check
Evaluate `((lambda (x) (+ x 1)) 2)` in your interpreter.
