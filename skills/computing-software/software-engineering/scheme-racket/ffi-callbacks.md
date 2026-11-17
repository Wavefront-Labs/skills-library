---
id: computing-software.software-engineering.scheme-racket.ffi-callbacks
name: ffi-callbacks
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, ffi-callbacks]
level: advanced
status: docs-checked
description: "Pass Racket procedures as C callbacks with function-ptr and _fun; keep them reachable or the GC may collect them."
sources:
  - https://docs.racket-lang.org/foreign/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Callbacks and lifetimes
**Goal:** safe callbacks.
```racket
(define cmp (_fun _pointer _pointer -> _int))
(define (my-cmp a b) 0)
(define cb (function-ptr my-cmp cmp))
```
- Store the callback in a long-lived binding if C holds it past the call (`#:keep`/`'#:keep`, see docs).
- Callbacks from other OS threads need async support (`#:async-apply`).
## Self-check
Use qsort from libc with a Racket comparator on an int array.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
