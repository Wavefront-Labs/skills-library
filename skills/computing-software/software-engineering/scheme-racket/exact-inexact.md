---
id: computing-software.software-engineering.scheme-racket.exact-inexact
name: exact-inexact
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, exact-inexact]
level: practitioner
status: docs-checked
description: "Convert and round numbers: exact->inexact, inexact->exact, round, exact-round and quotient/remainder versus modulo."
sources:
  - https://docs.racket-lang.org/reference/number-types.html
  - https://docs.racket-lang.org/reference/generic-numbers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exactness and rounding
**Goal:** convert safely.
- `(round 2.5)` is `2.0`: `round` returns the integer closest to `x`, resolving ties in favour of an even number. `exact-round` (from `racket/math`, not `racket/base`) is equivalent to `(inexact->exact (round x))`, so `(exact-round 2.5)` is `2`.
- `quotient` returns `(truncate (/ n m))`; `remainder` returns a result with the same sign as `n`; `modulo` returns a result with the same sign as `m`. All three take integers; `modulo` raises `exn:fail:contract:divide-by-zero` if `m` is exact 0, `0.0` or `-0.0`.
- `inexact->exact` coerces to an exact number (raising `exn:fail:contract` for `+inf.0`, `-inf.0` and `+nan.0`); `exact->inexact` coerces to an inexact number.
- `(rationalize x tolerance)` returns, among the numbers within `tolerance` of `x`, the one with the smallest denominator.
- Advice: keep values exact for money-like work, because inexact results are approximations.
## Self-check
`(modulo -7 3)` is `2` and `(remainder -7 3)` is `-1`.

## Checked
2026-11-08. Read: Racket Reference 4.3.1 Number Types (reference/number-types.html) entries `inexact->exact` and `exact->inexact`; in 4.3.2 Generic Numerics (reference/generic-numbers.html) the `quotient`, `remainder`, `modulo`, `round`, `rationalize` and `=` entries and the racket/math `exact-round` entry (the pages were searched for these entries, not read end to end). Removed the claim that `(inexact->exact 0.1)` is a large exact rational "not 1/10" (the pages give no such example) and the unsupported "parse the decimal text" suggestion; removed floor and truncate from the description since the body does not cover them. Replaced the guide/numbers and reference/numbers index sources.
Method: documentation only; no commands were run.
