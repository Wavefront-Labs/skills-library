---
id: computing-software.software-engineering.scheme-racket.r7rs-bytevectors
name: r7rs-bytevectors
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, r7rs-bytevectors, r7rs-small]
level: intro
status: docs-checked
description: "R7RS-small bytevectors (#u8 literals, bytevector-u8-ref, utf8->string, string->utf8) and digit-value, with the nearest Racket byte-string names."
sources:
  - https://small.r7rs.org/attachment/r7rs.pdf
  - https://docs.racket-lang.org/reference/bytestrings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# R7RS bytevectors and characters
**Goal:** binary data portably.
```scheme
(define b (bytevector 1 2 3))
(bytevector-u8-ref b 0) (utf8->string (string->utf8 "hi")) (digit-value #\7)
```
- Bytevectors are written `#u8(byte ...)` and are self-evaluating. `make-bytevector`, `bytevector`, `bytevector-length`, `bytevector-u8-ref`, `bytevector-u8-set!`, `bytevector-copy`, `bytevector-copy!` and `bytevector-append` are the core procedures.
- It is an error if `k` is not a valid index for `bytevector-u8-ref`, and an error for `utf8->string` to get invalid UTF-8.
- `digit-value` comes from the `(scheme char)` library.
- Nearest Racket names are `bytes`, `bytes-ref` and `bytes->string/utf-8`.
## Self-check
`(bytevector-length #u8(1 2 3))` is `3`.
## Checked
2026-11-08. Confirmed in the R7RS-small report, section 6.9 (Bytevectors) and Appendix A: all procedures, notation, error conditions and `digit-value` in `(scheme char)`; on the Racket Reference byte strings page: `bytes`, `bytes-ref`, `bytes->string/utf-8`. Removed: the unverified Racket `#u8(...)` literal claim.
Method: documentation only; no commands were run.
