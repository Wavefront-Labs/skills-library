---
id: computing-software.software-engineering.scheme-racket.let-forms
name: let-forms
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, let-forms, racket-binding]
level: intro
status: docs-checked
description: "Bind locals with let (parallel), let* (sequential) and letrec (mutually recursive)."
sources:
  - https://docs.racket-lang.org/guide/let.html
  - https://docs.racket-lang.org/reference/let.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# let, let* and letrec
**Goal:** choose the correct let.
```racket
(let ([a 1] [b 2]) (+ a b))
(let* ([a 1] [b (+ a 1)]) b)
(letrec ([even? (lambda (n) (if (zero? n) #t (odd? (- n 1))))]
         [odd?  (lambda (n) (if (zero? n) #f (even? (- n 1))))])
  (even? 10))
```
- In plain `let`, a binding's init cannot see sibling bindings.
- `let` bindings are made in parallel, so later bindings are not visible to earlier init expressions; `let*` makes each identifier available to later init expressions and allows repeated names.
- Racket also has `let-values`, `let*-values` and `letrec-values`.
## Self-check
`(let ([a 1] [b a]) b)` errors on unbound `a` (when no outer `a`).

## Checked

Date: 2026-11-02. Confirmed on Racket Guide Local Binding (parallel binding for `let`, sequential for `let*`) and the Reference for `let*-values` and `letrec-values`. Removed: nothing.

Method: documentation only; no commands were run.
