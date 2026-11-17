---
id: computing-software.software-engineering.scheme-racket.ffi-cstruct
name: ffi-cstruct
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, ffi-cstruct]
level: advanced
status: docs-checked
description: "Describe structs with define-cstruct, allocate with malloc, read with ptr-ref, and free manual allocations."
sources:
  - https://docs.racket-lang.org/foreign/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C structs and memory
**Goal:** exchange C data layouts.
```racket
(define-cstruct _pt ([x _int] [y _int]))
(define p (make-pt 1 2))
(pt-x p)
(define buf (malloc 16 'raw)) (ptr-set! buf _int 0 7) (ptr-ref buf _int 0) (free buf)
```
- `'raw` memory is not garbage collected; always `free`.
## Self-check
Round-trip an integer through `ptr-set!`/`ptr-ref`.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
