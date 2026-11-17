---
id: computing-software.software-engineering.scheme-racket.match-define
name: match-define
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, match-define]
level: practitioner
status: docs-checked
description: "Bind via patterns with match-define, match-let, match-lambda and match*."
sources:
  - https://docs.racket-lang.org/guide/match.html
  - https://docs.racket-lang.org/reference/match.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# match-define, match-let and match-lambda
**Goal:** concise destructuring.
```racket
(require racket/match)
(match-define (list a b) '(1 2))
(match-let ([(cons x y) '(1 . 2)]) (+ x y))
(define f (match-lambda [(list x) x] [_ #f]))
(match* (1 'a) [(1 'a) 'ok])
```
- `match-define` defines the names bound by the pattern to the values produced by matching the expression; `match-define-values` handles an expression that returns several values.
- `match-let` generalizes `let`: each pattern must match its expression, and the bindings are visible in the body. `match-let*` and `match-letrec` generalize `let*` and `letrec`.
- `(match-lambda clause ...)` is `(lambda (id) (match id clause ...))`; `match-lambda*` takes a rest list of arguments; `match-lambda**` is the multi-argument form based on `match*`.
- `match*` matches several values at once, and each clause needs one pattern per value.
## Self-check
`(match-let ([(list a b) '(1 2)] [(vector x ...) #(1 2 3 4)]) (list b a x))` returns `'(2 1 (1 2 3 4))`.

## Checked
2026-11-08. Confirmed on the Racket Reference section 9.1 (Additional Matching Forms) and the Racket Guide: `match-define`, `match-define-values`, `match-let` and variants, `match-lambda`, `match-lambda*`, `match-lambda**`, `match*`, and the self-check example. Removed the claim of the exact error text `match-define: no matching clause` and the old self-check about a failing `match-define`, since the pages do not state the failure message. Dropped "for/list with match-define" from the description; it is not covered.
Method: documentation only; no commands were run.
