---
id: computing-software.software-engineering.scheme-racket.syntax-case
name: syntax-case
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, syntax-case]
level: advanced
status: docs-checked
description: "Write Racket macros with syntax-case and #' templates; inspect syntax with syntax-e and syntax->datum and report errors with raise-syntax-error."
sources:
  - https://docs.racket-lang.org/guide/macros.html
  - https://docs.racket-lang.org/reference/stx-patterns.html
  - https://docs.racket-lang.org/reference/stxops.html
  - https://docs.racket-lang.org/reference/exns.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# syntax-case and syntax
**Goal:** macros with compile-time logic.
```racket
(require (for-syntax racket/base))
(define-syntax (my-if stx)
  (syntax-case stx ()
    [(_ c t e) #'(cond [c t] [else e])]))
```
- The form is `(syntax-case stx-expr (literal-id ...) clause ...)`; `(syntax template)`, written `#'template`, builds the result.
- The manual's `syntax-case` example first runs `(require (for-syntax racket/base))`, as needed for transformer code under `racket/base`.
- `syntax-e` and `syntax->datum` take a syntax object apart; `syntax->datum` returns a plain datum.
- `raise-syntax-error` takes a name, a message and optionally the offending expression and sub-expression.
## Self-check
Use `my-if` as `(my-if #t 1 2)` and confirm it returns `1`.
## Checked
2026-11-08. Confirmed on the Reference syntax-case and syntax-object pages: `syntax-case` and `syntax` forms, the `for-syntax racket/base` example, `syntax-e`, `syntax->datum`, and the `raise-syntax-error` signature (exns page). Removed: the `show-expr` macro and its `(+ 1 2) = 3` self-check (printf output not shown in the cited pages).
Method: documentation only; no commands were run.
