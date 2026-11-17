---
id: computing-software.software-engineering.scheme-racket.when-unless
name: when-unless
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, when-unless]
level: intro
status: docs-checked
description: "Run side effects conditionally with when/unless, whose bodies are implicit begins; they return void when the test fails."
sources:
  - https://docs.racket-lang.org/guide/begin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# when, unless and begin sequencing
**Goal:** one-armed conditionals.
```racket
(when (> n 0) (displayln "pos") (set! n (- n 1)))
(unless (file-exists? p) (error 'load "missing ~a" p))
```
- `when` evaluates its bodies if the test is true and returns the last body's value; otherwise the result is void, not `#f`.
- `unless` is the same with the test inverted: bodies run only when the test result is `#f`.
## Self-check
`(when #f 1)` prints nothing at the REPL.

## Checked

Date: 2026-11-02. Confirmed on Racket Guide Sequencing, section Effects If...: when and unless (void result when the test fails; `unless` inverts the test). Fixed sources (the conditionals page does not cover them).

Method: documentation only; no commands were run.
