---
id: computing-software.software-engineering.scheme-racket.ffi-functions
name: ffi-functions
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, ffi-functions]
level: advanced
status: docs-checked
description: "Describe C signatures with _fun, #:varargs-after, #:save-errno, and the define-ffi-definer macro for batches of bindings."
sources:
  - https://docs.racket-lang.org/foreign/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# _fun types and define-c
**Goal:** bind many functions.
```racket
(require ffi/unsafe ffi/unsafe/define)
(define-ffi-definer define-foo (ffi-lib "libfoo" '("2" #f)))
(define-foo foo_twice (_fun _int -> _int))
(foo_twice 4)
```
- Use `_string`, `_bytes`, `_pointer`, `_int32` etc. for exact widths.
- `#:fail (lambda () #f)` for optional symbols.
## Self-check
Bind one function from a shared library you have installed and call it.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
