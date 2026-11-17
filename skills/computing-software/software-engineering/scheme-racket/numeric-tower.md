---
id: computing-software.software-engineering.scheme-racket.numeric-tower
name: numeric-tower
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, numeric-tower, racket-numbers]
level: intro
status: docs-checked
description: "Racket numbers include exact integers of any size, exact rationals, flonums and complex numbers; know when results stay exact."
sources:
  - https://docs.racket-lang.org/guide/numbers.html
  - https://docs.racket-lang.org/reference/number-types.html
  - https://docs.racket-lang.org/reference/generic-numbers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric tower: integers, rationals, reals, complex
**Goal:** predict numeric types.
```racket
(/ 1 3)        ; 1/3 exact
(sqrt -1)      ; 0+1i exact complex
(exact->inexact 1/3)  ; 0.3333333333333333
(= 1/10 0.1)   ; #f
```
- A number is exact (arbitrarily large integers, exact rationals, complex numbers with exact parts) or inexact (IEEE floating point, including `+inf.0` and `+nan.0`, and complex numbers with float parts). Inexact input makes the result inexact.
- `sqrt` is exact when the argument is exact and its root is rational; otherwise inexact. `(sqrt 2)` is `1.4142135623730951`.
- Predicates: `integer? rational? real? complex? exact? inexact? fixnum? flonum?`. Every number is `complex?`; `fixnum?` is platform-dependent.
- `=` compares by numeric value across exactness, `eqv?` and `equal?` also compare exactness. `(= 1/2 0.5)` is `#t` but `(= 1/10 0.1)` is `#f`, because base-2 floats cannot represent 1/10, so compare floats with a tolerance.
- `abs` rejects complex numbers (contract violation); many other functions accept them.
## Self-check
`(integer? 2.0)` is `#t` but `(exact? 2.0)` is `#f`.

## Checked
2026-11-08. Confirmed on the Racket Guide section 3.2 (Numbers) and Racket Reference sections 4.3.1 and 4.3.2: exact / inexact definitions, inexact taint, `sqrt` exactness and `(sqrt -1)` result `0+1i`, `exact->inexact`, `=` versus `eqv?`, `(= 1/10 0.1)`, the predicate list and `fixnum?` platform dependence, `(integer? 4.0)`. Removed the bignum `expt` example (no `expt` text was on the pages read), the invalid `(= 0.1+0.2 0.3)` snippet and the `+2i` print form (the Reference prints `0+1i`).
Method: documentation only; no commands were run.
