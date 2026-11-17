---
id: computing-software.software-engineering.scheme-racket.unsafe-ops
name: unsafe-ops
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, unsafe-ops]
level: advanced
status: docs-checked
description: "Use racket/unsafe/ops (unsafe-fx+, unsafe-vector-ref) only in verified hot loops; unchecked arguments can crash or corrupt the whole system."
sources:
  - https://docs.racket-lang.org/guide/performance.html
  - https://docs.racket-lang.org/reference/unsafe.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# racket/unsafe/ops
**Goal:** last-resort speedups.
```racket
(require racket/unsafe/ops)
(unsafe-fx+ 1 2) (unsafe-vector-ref (vector 1 2) 0)
```
- These functions are like their `racket/base` counterparts but assume, instead of checking, that arguments have the right type and are in range (`unsafe-vector-ref` skips both the vector check and the bounds check). If a constraint is violated, behaviour is unpredictable: the whole system can crash or become corrupted.
- `unsafe-fx+` takes fixnums and returns a fixnum; since 7.0.0.13 it accepts zero or more arguments. There is also `unsafe-fx+/wraparound`. `unsafe-vector*-ref` additionally requires a non-impersonator vector.
- Benefits vary by function and context, so profile first. The Guide says unchecked flonum-specific operations allow unboxing and sometimes let the compiler reorder expressions; `racket/flonum` operations already allow unboxing with checks, so try those first.
- All bindings are protected like `protect-out`, so a code inspector can block access to unsafe operations.
## Self-check
Benchmark a vector sum with safe versus unsafe ops, with indices known to be in range.

## Checked
2026-11-08. Confirmed against Racket Guide section 19.9 (Unchecked, Unsafe Operations) and the Reference page Unsafe Operations: crash/corruption warning, unsafe-vector-ref semantics, unsafe-fx+ argument change note, wraparound variant, protect-out note, flonum unboxing remarks. Removed: the claim that `racket/fixnum` safe ops are an alternative (the Guide cites only racket/flonum for unboxing).
Method: documentation only; no commands were run.
