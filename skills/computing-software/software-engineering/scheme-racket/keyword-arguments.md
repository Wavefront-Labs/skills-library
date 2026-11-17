---
id: computing-software.software-engineering.scheme-racket.keyword-arguments
name: keyword-arguments
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, keyword-arguments]
level: practitioner
status: docs-checked
description: "Declare and call keyword arguments with #:name in define and lambda, including required and optional keywords."
sources:
  - https://docs.racket-lang.org/guide/lambda.html
  - https://docs.racket-lang.org/guide/apply.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyword arguments
**Goal:** order-independent named arguments.
```racket
(define (box-area #:w w #:h [h 1]) (* w h))
(box-area #:h 3 #:w 2)   ; => 6
(apply box-area #:w 2 '())  ; keywords given to apply itself
(keyword-apply box-area '(#:w) '(2) '())  ; keywords from lists
```
- `#:w w` declares a keyword argument without a default and `#:h [h 1]` one with a default; the position of a keyword and its argument in the formals does not matter when matching a call.
- Keywords inside the list given to `apply` count as positional arguments, so they do not reach the keyword parameters.
- `keyword-apply` takes the function and three lists: keywords (sorted by `keyword<?`), a parallel list of their values, and the positional arguments.
## Self-check
`(box-area #:h 3 #:w 2)` and `(box-area #:w 2 #:h 3)` both give `6`.

## Checked

Date: 2026-11-02. Confirmed on Racket Guide Functions: lambda (Declaring Keyword Arguments) and The apply Function (apply passes its own keywords along; keywords in its list are positional; keyword-apply with sorted keyword list). Fixed: the example `(apply box-area '(#:w 2))` passes `#:w` as a positional argument, so it fails; replaced with correct forms. Removed: the speed claim and the missing-keyword error wording.

Method: documentation only; no commands were run.
