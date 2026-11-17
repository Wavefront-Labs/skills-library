---
id: computing-software.software-engineering.scheme-racket.for-fold
name: for-fold
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, for-fold]
level: practitioner
status: docs-checked
description: "Accumulate state with for/fold, including multiple accumulators and #:result, as the functional replacement for loops with mutation."
sources:
  - https://docs.racket-lang.org/guide/for.html
  - https://docs.racket-lang.org/reference/for.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# for/fold accumulators
**Goal:** immutable loop state.
```racket
(for/fold ([sum 0] [n 0]) ([x '(3 4 5)])
  (values (+ sum x) (add1 n)))      ; 12 and 3 as two values
(for/fold ([acc '()] #:result (reverse acc)) ([x '(1 2 3)]) (cons x acc))
```
- The last body expression must produce as many values as there are accumulators, and `for/fold` itself returns that many values.
- With `#:result result-expr`, the result is `result-expr`, evaluated with the accumulators bound to their final values; otherwise the results are the accumulator values.
- `#:result` was added in Racket 6.11.0.1. Accumulators are not visible in the outermost `for` clauses' sequence expressions.
- `for*/fold` nests clauses like `for*`; `for/foldr` runs the body in reverse order at the cost of space proportional to the iterations.
## Self-check
Compute max and min of a list in one `for/fold` pass.

## Checked
2026-11-08. Confirmed on the Racket Reference section 3.18 (for/fold, for/foldr entries) and Racket Guide section 11.7: multiple accumulators and values, `#:result` semantics, the "Added the #:result form" note for 6.11.0.1, and for/foldr space behaviour. Replaced the vague "Racket 7+/8" version note with the documented version; replaced the sequences page with the Reference for page. The accumulator-scope sentence follows the Reference text on outermost for-clauses.
Method: documentation only; no commands were run.
