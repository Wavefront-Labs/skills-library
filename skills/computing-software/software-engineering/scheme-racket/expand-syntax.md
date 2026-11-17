---
id: computing-software.software-engineering.scheme-racket.expand-syntax
name: expand-syntax
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, expand-syntax]
level: practitioner
status: docs-checked
description: "Inspect macro output with expand, expand-once, expand-to-top-form and syntax->datum in a namespace."
sources:
  - https://docs.racket-lang.org/macro-debugger/
  - https://docs.racket-lang.org/reference/Expanding_Top-Level_Forms.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# expand, syntax->datum and expand-once
**Goal:** read what a macro produces.
```racket
(define ns (make-base-namespace))
(syntax->datum (parameterize ([current-namespace ns]) (expand '(let ([x 1]) x))))
```
- `expand` expands all non-primitive syntax and returns a syntax object containing only core forms; use `syntax->datum` to make it printable.
- `expand-once` partially expands the form. The manual warns that calling `expand-once` on its result can differ from full expansion via `expand`.
- `expand-to-top-form` partially expands to reveal the outermost syntactic form (mainly for spotting top-level `begin`); unlike `expand-once`, expanding its result with `expand` gives the same result as expanding the original.
- The macro-debugger manual shows fully expanded output using core forms such as `let-values` and `#%app`.
## Self-check
Expand `(let ([x 1] [y 2]) (or (even? x) (even? y)))` and look for `let-values` and `#%app` in the result.
## Checked
2026-11-08. Confirmed on the Reference page Expanding Top-Level Forms: the behaviour of `expand`, `expand-once` and `expand-to-top-form` and the use of `syntax->datum`; on the macro-debugger page: the example output with `let-values` and `#%app`. Removed: "expand-once expands only the outermost macro use" (page says "partially expands"), "expand-to-top-form stops at a core form", and the `(when #t 1)` self-check (its expansion is not shown on the pages).
Method: documentation only; no commands were run.
