---
id: computing-software.software-engineering.scheme-racket.accumulator-recursion
name: accumulator-recursion
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, accumulator-recursion]
level: practitioner
status: docs-checked
description: "Convert linear recursion to accumulator style with an inner iter helper; accumulated lists come out reversed, so reverse at the end."
sources:
  - https://docs.racket-lang.org/guide/Lists__Iteration__and_Recursion.html
  - https://docs.racket-lang.org/reference/eval-model.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accumulators
**Goal:** refactor recursion into constant-space loops.
```racket
(define (fact n)
  (define (iter n acc) (if (zero? n) acc (iter (sub1 n) (* acc n))))
  (iter n 1))
(define (my-map f lst)
  (define (iter lst backward-result)
    (cond [(empty? lst) (reverse backward-result)]
          [else (iter (rest lst) (cons (f (first lst)) backward-result))]))
  (iter lst empty))
```
- Plain linear recursion stacks up pending operations (`(+ 1 ...)` per element). Adding along the way in an extra argument makes each recursive call the result of the enclosing call, so it runs in constant space under the tail-call guarantee.
- The Guide's pattern is a local `iter` function that carries the accumulator, with the outer function calling it with the initial value.
- An accumulated list is backwards, so `reverse` it at the very end. For `my-map` O(n) space is reasonable anyway since the result is O(n); reversing only reduces a constant factor, and the Guide says that is usually not worthwhile. `for/list` expands to essentially the same code.
- Racket programmers embrace plain recursion: there is no stack overflow, only running out of memory with far deeper recursion than other languages allow.
## Self-check
`(fact 20)` equals `2432902008176640000`.

## Checked
2026-11-08. Confirmed against Racket Guide section 2.3 (iter accumulator example, reverse at the end, for/list equivalence, recursion versus iteration) and the Reference's tail-position definition. Removed: the optional-argument `fact` signature and the `ev?`/`od?` mutual-recursion claim (not on pages read); the SICP source (unreadable).
Method: documentation only; no commands were run.
