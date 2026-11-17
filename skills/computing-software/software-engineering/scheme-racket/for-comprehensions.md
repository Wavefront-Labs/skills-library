---
id: computing-software.software-engineering.scheme-racket.for-comprehensions
name: for-comprehensions
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, for-comprehensions, racket-for-loops]
level: intro
status: docs-checked
description: "Iterate with for, for/list, for/vector, for/hash, for/sum, for/and, using in-range, in-list and #:when / #:break clauses."
sources:
  - https://docs.racket-lang.org/guide/for.html
  - https://docs.racket-lang.org/reference/for.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# for, for/list and friends
**Goal:** idiomatic iteration.
```racket
(for/list ([i (in-range 5)] #:when (odd? i)) (* i i))   ; '(1 9)
(for/sum ([x '(1 2 3)]) x)
(for/hash ([k '(a b)] [v (in-naturals)]) (values k v))
(for* ([i 3] [j 3]) (displayln (list i j)))   ; nested
(for ([x '(1 2 3)] #:break (> x 2)) (displayln x))
```
- Parallel clauses `[a ...] [b ...]` stop when the shortest sequence ends; `for*` nests them instead.
- `for/hash` bodies must return two values (key and value); `for/sum` accumulates with `+`; `for/and` stops at the first `#f`.
- `#:when` / `#:unless` skip the body (and, in `for/list`, add no element); `#:break` ends all sequences.
- A bare number `k` is a sequence like `(in-range k)`. Using `in-list`, `in-vector`, `in-range` or a literal in the clause lets `for` compile to a fast loop; an arbitrary sequence value is dispatched at run time and is slower.
## Self-check
`(for/list ([i 3] [c "ab"]) (cons i c))` has two elements.

## Checked
2026-11-08. Confirmed on the Racket Guide section 11 (Iterations and Comprehensions) and Racket Reference section 3.18: `for`, `for*`, `for/list`, `for/vector`, `for/hash` (two-value body), `for/sum`, `for/and`, `#:when`, `#:unless`, `#:break`, parallel iteration ending with the shortest sequence, numbers as `in-range`, and the fast-clause rule with `in-list` / `in-vector`. Replaced the Reference sequences page with the Reference for page as the source for `for/hash` and `for/sum`.
Method: documentation only; no commands were run.
