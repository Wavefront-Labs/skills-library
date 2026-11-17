---
id: computing-software.software-engineering.scheme-racket.tail-calls
name: tail-calls
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, tail-calls, racket-recursion]
level: practitioner
status: docs-checked
description: "Racket guarantees that expressions in tail position take no extra space, so tail-recursive loops run in constant space; know which forms give tail positions."
sources:
  - https://docs.racket-lang.org/reference/eval-model.html
  - https://docs.racket-lang.org/guide/Lists__Iteration__and_Recursion.html
  - https://docs.racket-lang.org/reference/if.html
  - https://docs.racket-lang.org/reference/begin.html
  - https://docs.racket-lang.org/reference/let.html
  - https://docs.racket-lang.org/reference/lambda.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proper tail calls
**Goal:** know what is a tail call.
```racket
(define (len l acc) (if (null? l) acc (len (cdr l) (add1 acc))))  ; tail call
(define (bad l) (if (null? l) 0 (+ 1 (bad (cdr l)))))             ; not tail
```
- Definition: expr1 is in tail position with respect to expr2 if, whenever expr1 becomes a redex, its continuation is the same as expr2's. `(+ 1 1)` is not in tail position in `(- 4 (+ 1 1))`.
- It is a guarantee, not an optimisation: an expression in tail position does not take extra computation space over the enclosing expression.
- Tail positions per the Reference: both branches of `if`; the last body of a `cond` clause (and a `cond` `=>` procedure application) but not the clause's test-expr; the last `expr` of `and` / `or`; the last body expression of a `lambda` or `let`; the last `expr` of `begin` (`begin0`: only if it is the sole expr); the handler call of `with-handlers*`.
- `(bad l)` stacks up one pending `(+ 1 ...)` per element, so it uses O(n) space; the Guide notes that there is no stack overflow in Racket, but a computation with too much context can run out of memory.
- Prefer a tail-recursive helper (or `for` forms) when a computation can run in constant space.
## Self-check
Run `len` and `bad` on a list of a million elements and compare memory use.

## Checked
2026-11-08. Confirmed against the Reference pages Evaluation Model (Tail Position), if/cond/and/or, begin, let, lambda, and the Guide section 2.3 (Lists, Iteration, and Recursion): definition, guarantee wording, listed tail positions, no stack overflow. Removed: tail positions for `when`/`unless`, and the "not tail" claims for `with-handlers`, `parameterize` and `dynamic-wind` (not on any page read); the SICP source (unreadable).
Method: documentation only; no commands were run.
