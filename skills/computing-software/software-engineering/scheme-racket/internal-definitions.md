---
id: computing-software.software-engineering.scheme-racket.internal-definitions
name: internal-definitions
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, internal-definitions]
level: practitioner
status: docs-checked
description: "Use define inside lambda and other body positions; internal definitions are mutually recursive, but referencing one before it is evaluated is an error."
sources:
  - https://docs.racket-lang.org/guide/define.html
  - https://docs.racket-lang.org/reference/define.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Internal definitions
**Goal:** structure local helpers.
```racket
(define (f n)
  (define sq (* n n))
  (define (half x) (/ x 2))
  (half sq))
```
- Wherever a form's grammar says `body` (for example `lambda` and the function shorthand of `define`), the body can mix definitions and expressions; a definition used as a body is an internal definition.
- The last body must be an expression.
- Internal definitions in one body are mutually recursive: any can refer to any other, as long as the reference is not evaluated before its definition. A too-early reference is an error. `(define (weird) (define x x) x)` fails with `x: undefined; cannot use before initialization`.
- A sequence of internal definitions made only with `define` translates to an equivalent `letrec`; other definition forms such as `define-values`, `struct` and `define-syntax` can also appear.
- In an internal-definition context `define`, `define-values`, `define-syntax` and `define-syntaxes` introduce local bindings.
## Self-check
Call `(weird)` from the example above and confirm the use-before-initialization error.

## Checked
2026-11-08. Confirmed on the Racket Guide section 4.5.4 (Internal Definitions) and the Racket Reference definitions page (`define`, `define-values`, `define-syntax` in internal-definition contexts). Removed the `letrec*` equivalence (the Guide says `letrec`), the invented error text "variable used before its definition", the claim that `begin` splices definitions, and the `when` / `cond` body claim, none of which these pages state. The Reference's separate Internal Definitions section was not part of this check.
Method: documentation only; no commands were run.
