---
id: computing-software.software-engineering.scheme-racket.define-forms
name: define-forms
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, define-forms, racket-definitions]
level: intro
status: docs-checked
description: "Bind names with define (variables and functions), update with set!, and know that set! on an undefined identifier is an error."
sources:
  - https://docs.racket-lang.org/guide/define.html
  - https://docs.racket-lang.org/reference/define.html
  - https://docs.racket-lang.org/guide/module-set.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# define, define-values and set!
**Goal:** define and mutate bindings.
```racket
(define x 10)
(define (sq n) (* n n))
(define ((adder a) b) (+ a b))   ; curried define: ((adder 1) 2) => 3
(set! x (+ x 1))
```
- A module may `set!` its own definitions, and importers see the change; an importing context may not `set!` an imported binding, so export a mutator function instead.
- The curried shorthand `(define ((adder a) b) ...)` defines a function that returns a function.
## Self-check
`(define ((adder a) b) (+ a b))` then `((adder 1) 2)` gives `3`.

## Checked

Date: 2026-11-02. Confirmed on Racket Guide Definitions (curried function shorthand) and 6.6 Assignment and Redefinition (set! only within the defining module; mutator functions). Removed: the redefinition and optimisation claims and the existing-binding claim, which these pages do not state.

Method: documentation only; no commands were run.
