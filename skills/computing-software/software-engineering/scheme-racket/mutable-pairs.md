---
id: computing-software.software-engineering.scheme-racket.mutable-pairs
name: mutable-pairs
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, mutable-pairs]
level: practitioner
status: docs-checked
description: "Know that Racket pairs are immutable; use mcons/set-mcar!/set-mcdr! only when mutation is required."
sources:
  - https://docs.racket-lang.org/guide/pairs.html
  - https://docs.racket-lang.org/reference/mpairs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mutable pairs (mcons)
**Goal:** avoid set-car! assumptions.
```racket
(define p (mcons 1 2))
(set-mcar! p 10)
(mpair? p)   ; #t   (pair? p) is #f
```
- Pairs made by `cons` are immutable; `pair?` and `list?` recognize only immutable pairs and lists.
- A mutable pair is a separate datatype, not a pair: use `mcons`, `mcar`, `mcdr`, `set-mcar!`, `set-mcdr!` and `mpair?`. The empty list is also the empty mutable list.
- `write` and `display` print a mutable pair with braces, for example `{0 . 2}`; the REPL prints it as `(mcons 0 2)`.
- The Reference advises pairs, lists and hash tables over mutable pairs and lists in almost every case. A mutable list can serve as a sequence via `in-mlist`.
## Self-check
`(pair? (mcons 1 2))` is `#f`.

## Checked
2026-11-08. Confirmed on the Racket Guide pairs page and Racket Reference section 4.11 (Mutable Pairs and Lists): immutability of `cons` pairs, `mcons` / `mcar` / `mcdr` / `set-mcar!` / `set-mcdr!` / `mpair?`, `pair?` being `#f` for mutable pairs, brace printing with `write`, `in-mlist`, and the advice to prefer other structures. Removed the claims about `set-car!` being absent, R7RS code needing the `r7rs` language, and `#lang scheme` / `mzscheme` differences, none of which these pages state.
Method: documentation only; no commands were run.
