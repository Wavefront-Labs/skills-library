---
id: computing-software.software-engineering.scheme-racket.macro-phases
name: macro-phases
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, macro-phases]
level: advanced
status: docs-checked
description: "Compile-time versus run-time phase levels: begin-for-syntax bindings sit at phase 1, and (require (for-syntax ...)) imports at one phase higher."
sources:
  - https://docs.racket-lang.org/guide/macros.html
  - https://docs.racket-lang.org/reference/syntax-model.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Phase levels and begin-for-syntax
**Goal:** share code with macros.
```racket
(require (for-syntax racket/base))
(begin-for-syntax (define (double n) (* 2 n)))
(define-syntax (k stx) (datum->syntax stx (double 21)))
```
- An identifier can have different bindings at different phase levels.
- The expression of a `define-syntaxes` transformer is expanded and evaluated at phase level 1.
- `begin-for-syntax` at module or top level introduces bindings at phase level 1; nested `begin-for-syntax` forms each shift by one more level.
- `(require (for-syntax ...))` imports bindings one phase level higher, and the expander instantiates the required module at phase 1 immediately.
## Self-check
Move `double` out of `begin-for-syntax` into a plain `define`, and see how the binding at phase 0 differs from the one the transformer sees at phase 1.
## Checked
2026-11-08. Confirmed on the Reference syntax-model page: per-phase bindings, `define-syntaxes` transformer expressions expanded at phase level 1, `begin-for-syntax` phase-1 bindings and nesting, and `for-syntax` import shifting and immediate instantiation; the Guide macros page lists the phase sections. Removed: `define-for-syntax` (not on the cited pages) and the statements that run-time definitions are invisible at phase 1 and that a specific unbound error results.
Method: documentation only; no commands were run.
