---
id: computing-software.software-engineering.scheme-racket.optional-arguments
name: optional-arguments
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, optional-arguments, racket-procedures]
level: intro
status: docs-checked
description: "Give parameters defaults with (define (f a [b 10]) ...); later optionals may refer to earlier arguments."
sources:
  - https://docs.racket-lang.org/guide/lambda.html
  - https://docs.racket-lang.org/guide/application.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optional arguments
**Goal:** write functions with defaults.
```racket
(define (greet name [greeting "hello"] [punct "!"])
  (string-append greeting " " name punct))
(greet "ann") (greet "ann" "hi")
```
- An argument written `[arg-id default-expr]` is optional, and every following argument must also have a default.
- A default expression can refer to any preceding argument: `[c (+ a b)]`.
## Self-check
`(greet "ann")` returns `"hello ann!"`.

## Checked

Date: 2026-11-02. Confirmed on Racket Guide Functions: lambda, Declaring Optional Arguments (defaults, following arguments need defaults, defaults may use preceding arguments). Removed: the 'positional' wording.

Method: documentation only; no commands were run.
