---
id: computing-software.software-engineering.fortran.cache-friendly-loops
name: cache-friendly-loops
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, cache-friendly-loops, fortran-performance]
level: practitioner
status: draft
description: "Order loops for column-major access, use array-of-structures vs structure-of-arrays carefully, and block loops."
sources:
  - https://gcc.gnu.org/onlinedocs/gfortran/
  - https://gcc.gnu.org/onlinedocs/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cache-friendly loops and layout
**Goal:** speed up memory-bound code.
- Innermost loop over the first index; avoid strided access.
- Prefer structure-of-arrays (separate arrays per field) for vectorisation over arrays of derived types.
- Block (tile) matrix loops for cache reuse; or call BLAS.
```fortran
do jj = 1, n, nb
  do ii = 1, n, nb
    do j = jj, min(jj+nb-1, n)
      do i = ii, min(ii+nb-1, n)
        b(i, j) = a(j, i)
```
- Use `-O3 -march=native` and check `-fopt-info-vec` after restructuring.
- Measure; do not guess.
## Gotchas
- Block size is hardware dependent; tune empirically.
- Compilers may interchange loops (`-floop-interchange`) at higher optimisation but not reliably.
## Self-check
Benchmark transposed vs untransposed loop order and record speedup.
