---
id: computing-software.software-engineering.scheme-racket.cond-case
name: cond-case
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, cond-case, racket-conditionals]
level: intro
status: docs-checked
description: "Branch with if, cond (including => and else), and case for eqv?-comparable literals."
sources:
  - https://docs.racket-lang.org/guide/conditionals.html
  - https://docs.racket-lang.org/reference/case.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# if, cond and case
**Goal:** pick the right conditional form.
```racket
(cond [(assv 2 '((1 . a) (2 . b))) => cdr]
      [(< 1 0) 'neg]
      [else 'other])
(case x [(1 2 3) 'low] [(a b) 'sym] [else 'other])
```
- `if` needs both branches; use `when`/`unless` for one-armed.
- `case` compares with `equal?` in Racket and its datums are literals (not evaluated).
- `=>` passes the test value to a procedure.
## Self-check
`(cond [#f 1])` returns void, no else.

## Checked

Date: 2026-11-02. Confirmed on Racket Guide Conditionals (`if` needs both branches and `when`/`unless` for one-armed; `=>` passes the test value to a one-argument procedure; `cond` without `else` gives void) and Racket Reference Dispatch: case (datums are quoted and compared with `equal?`; no match and no `else` gives void). Removed: nothing.

Method: documentation only; no commands were run.
