---
id: computing-software.software-engineering.scheme-racket.vector-operations
name: vector-operations
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, vector-operations, racket-vectors]
level: intro
status: docs-checked
description: "Create and use Racket vectors with make-vector, vector-ref, vector-set!, for/vector and vector->list; literals are immutable and vector-set! on them raises exn:fail:contract."
sources:
  - https://docs.racket-lang.org/guide/vectors.html
  - https://docs.racket-lang.org/reference/vectors.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vector operations
**Goal:** random-access arrays.
```racket
(define v (make-vector 3 0))
(vector-set! v 0 'a)
(vector-ref v 0)
(for/vector ([i (in-range 5)]) (* i i))
(vector->list v)
```
- A vector is mutable or immutable. Vectors from the default reader (such as a literal `#(1 2)`) are immutable, as are results of `vector-immutable`; giving an immutable vector to `vector-set!` raises `exn:fail:contract`.
- `make-vector` with one fill value shares that value across all slots, so `(make-vector 3 (make-vector 4))` is a poor mutable 3x4 matrix; use `for/vector` so each row is built separately.
- `vector-copy`, `vector-map` and `vector-sort` are documented with `racket/vector` (also provided by `racket`, not by `racket/base`).
## Self-check
`(vector-set! #(1 2) 0 9)` raises a contract error (`exn:fail:contract`).
## Checked
2026-11-08. Confirmed on the Reference vectors page: mutable versus immutable vectors, reader-produced vectors being immutable, `exn:fail:contract` for `vector-set!` on an immutable vector, `vector-immutable`, the `make-vector` sharing warning with the `for/vector` fix, and `vector-copy`/`vector-map`/`vector-sort` appearing in the `racket/vector` section; and on the Guide vectors page that literals are immutable. Removed: the claim that bounds errors raise `exn:fail:contract` (not stated for `vector-ref`/`vector-set!` on the cited pages), and the bare `[i 5]` sequence in `for/vector` (replaced by the documented `in-range` form).
Method: documentation only; no commands were run.
