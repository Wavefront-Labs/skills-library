---
id: computing-software.software-engineering.scheme-racket.specialized-vectors
name: specialized-vectors
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, specialized-vectors]
level: advanced
status: docs-checked
description: "Use racket/flonum flvectors and racket/fixnum fxvectors with fl+ and fx+ operations for unboxed numeric arrays."
sources:
  - https://docs.racket-lang.org/reference/flonums.html
  - https://docs.racket-lang.org/reference/fixnums.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# flvectors and fxvectors
**Goal:** faster numeric loops.
```racket
(require racket/flonum)
(define a (make-flvector 3 0.0))
(flvector-set! a 0 1.5)
(fl+ (flvector-ref a 0) 2.0)
```
- `racket/flonum` operations such as `fl+` consume and produce only flonums (their arguments are specified as `flonum?`); they are as safe as generic `+`, and flonum-specific operations can perform better when used consistently.
- An `flvector` holds only inexact real numbers; the representation can be more compact, and unsafe operations on flvectors (`racket/unsafe/ops`) can run more efficiently than unsafe operations on vectors of inexact reals. `make-flvector` takes a size and optional fill value.
- `racket/fixnum` provides `fx+`, `make-fxvector` and friends. Its operations are safe versions of the unsafe `unsafe-fx+` family and are generally no faster than generic `+`; `fx+` raises `exn:fail:contract:non-fixnum-result` if the result is not a fixnum (the `fx+/wraparound` variants discard overflow bits instead).
- Measure before switching; the docs give no blanket speed-up figure.
## Self-check
`(fl+ 1 2.0)` should be rejected because `1` is not a flonum (use `1.0`).

## Checked
2026-11-08. Confirmed against the Reference pages for flonums and fixnums (racket/flonum, racket/fixnum): flonum-only operations and safety, flvector description, `make-flvector`, `flvector-ref`, `flvector-set!`, `make-fxvector`, safe versus unsafe fixnum operations, `exn:fail:contract:non-fixnum-result`, `fx+/wraparound`.
Removed: "unless unsafe mode", the claim that gains show mostly in Racket CS (not stated), and the vectors pages as sources of those claims. The exact error text of `(fl+ 1 2.0)` is not shown in the docs, so the self-check says only that it is rejected.
Method: documentation only; no commands were run.
