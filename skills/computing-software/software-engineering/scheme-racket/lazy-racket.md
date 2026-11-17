---
id: computing-software.software-engineering.scheme-racket.lazy-racket
name: lazy-racket
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, lazy-racket]
level: advanced
status: docs-checked
description: "Use #lang lazy where function applications delay arguments until needed, with ! to force and !! for deep force."
sources:
  - https://docs.racket-lang.org/lazy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lazy Racket
**Goal:** lazy semantics in Racket.
```racket
#lang lazy
(define (ints n) (cons n (ints (add1 n))))
(! (list-ref (ints 0) 5))
```
- Function applications are delayed and promises are forced automatically (call-by-need). Primitives are strict where expected, struct constructors are lazy, and `if`, `and`, `or` are plain lazy functions.
- Strict, as-is functionality: `begin`, I/O, mutation, parameterization. Chain side effects in `begin` where order matters, and be aware of when promises are forced.
- Forcing (from `lazy/force`, re-provided by `lazy`): `!` forces an expression until it is a non-promise, `!!` also forces structures recursively, `!list` forces the cdrs of a list, `!!list` also forces the elements.
- Mixing with strict code: imported functions not defined in the lazy language are treated as strict; on the strict side you only need to force (possibly recursively) through promises.
- `cycle` builds a lazy infinite list repeating its arguments.
## Self-check
An infinite list defined with plain `cons` works under `#lang lazy`.

## Checked
2026-11-08. Confirmed against the Lazy Racket manual: language overview, strict versus lazy bindings, the forcing procedures `!`, `!!`, `!list`, `!!list`, `cycle`, mixing with strict code.
Removed: "I/O needs `!` forcing" (the docs say I/O is strict and side effects should be chained in `begin`), the `racket/lazy` helper claim (no such module is documented), and the Typed Racket guide as a source.
Method: documentation only; no commands were run.
