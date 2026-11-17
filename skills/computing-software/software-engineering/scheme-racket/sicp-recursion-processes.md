---
id: computing-software.software-engineering.scheme-racket.sicp-recursion-processes
name: sicp-recursion-processes
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sicp-recursion-processes]
level: intro
status: draft
description: "Distinguish recursive and iterative processes with factorial and Fibonacci, orders of growth, and counting change (SICP 1.2)."
sources:
  - https://sarabander.github.io/sicp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Linear recursion vs iteration
**Goal:** reason about process shape.
```racket
(define (fib n) (let loop ([a 0] [b 1] [i n]) (if (zero? i) a (loop b (+ a b) (sub1 i)))))
```
- Naive tree-recursive `fib` is exponential; the iterative form is linear time, constant space.
- A recursive procedure can generate an iterative process when it is tail-recursive.
## Self-check
Time `(fib 35)` naive versus loop.
