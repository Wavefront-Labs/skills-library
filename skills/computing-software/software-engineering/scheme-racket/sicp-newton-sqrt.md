---
id: computing-software.software-engineering.scheme-racket.sicp-newton-sqrt
name: sicp-newton-sqrt
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sicp-newton-sqrt, sicp-procedures]
level: intro
status: draft
description: "Build sqrt by successive approximation (good-enough?, improve, sqrt-iter) as in SICP section 1.1.7 and see block structure."
sources:
  - https://sarabander.github.io/sicp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Newton's method square root
**Goal:** procedural abstraction.
```racket
(define (sqrt-iter g x)
  (if (< (abs (- (* g g) x)) 0.001) g (sqrt-iter (/ (+ g (/ x g)) 2) x)))
(sqrt-iter 1.0 9)
```
- Fixed tolerance fails for very small and very large numbers; compare successive guesses relative to the guess instead.
- Internal definitions hide helpers (block structure).
## Self-check
Compare against `sqrt` for 1e-10 and 1e20 and note the fixed-tolerance error.
