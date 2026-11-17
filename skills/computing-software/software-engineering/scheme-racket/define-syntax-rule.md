---
id: computing-software.software-engineering.scheme-racket.define-syntax-rule
name: define-syntax-rule
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, define-syntax-rule, racket-syntax-rules]
level: intro
status: docs-checked
description: "Write simple macros with define-syntax-rule: a pattern and a template, expanded at compile time."
sources:
  - https://docs.racket-lang.org/guide/macros.html
  - https://docs.racket-lang.org/guide/pattern-macros.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# define-syntax-rule
**Goal:** define a new syntactic form.
```racket
(define-syntax-rule (swap! a b) (let ([t a]) (set! a b) (set! b t)))
(define-syntax-rule (my-unless c body ...) (if c (void) (begin body ...)))
```
- `(define-syntax-rule pattern template)` matches a use of the form against the pattern and replaces it with the template.
- Macro expansion is hygienic: a template-introduced `t` does not capture a user variable named `t`.
## Self-check
`(let ([x 1] [y 2]) (swap! x y) (list x y))` gives `'(2 1)`.

## Checked

Date: 2026-11-02. Confirmed on Racket Guide Pattern-Based Macros (`define-syntax-rule pattern template`, the swap example, hygiene with a temporary named `tmp`). Removed: the function-versus-macro advice.

Method: documentation only; no commands were run.
