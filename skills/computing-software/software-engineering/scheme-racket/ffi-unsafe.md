---
id: computing-software.software-engineering.scheme-racket.ffi-unsafe
name: ffi-unsafe
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, ffi-unsafe, racket-ffi]
level: advanced
status: docs-checked
description: "Call C shared libraries with ffi/unsafe: ffi-lib, get-ffi-obj and _fun types; mistakes can crash the process."
sources:
  - https://docs.racket-lang.org/foreign/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ffi/unsafe basics: ffi-lib and get-ffi-obj
**Goal:** call a C function.
```racket
(require ffi/unsafe)
(define libc (ffi-lib #f))          ; process libs (libc on most Unixes)
(define c-abs (get-ffi-obj "abs" libc (_fun _int -> _int)))
(c-abs -5)   ; 5
```
- `(ffi-lib "libfoo" '("2" #f))` tries version 2, then falls back to the unversioned library.
- Wrong types or signatures cause crashes, not exceptions.
- Windows C runtime library names differ (confirm for your toolchain).
## Self-check
Call `abs` and `strlen` via FFI.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
