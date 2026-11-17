---
id: computing-software.software-engineering.fortran.vectorization-lto
name: vectorization-lto
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, vectorization-lto, fortran-performance]
level: advanced
status: docs-checked
description: "Read vectorisation reports and use -flto and the ivdep directive to enable optimisation across files."
sources:
  - https://gcc.gnu.org/onlinedocs/gfortran/
  - https://gcc.gnu.org/onlinedocs/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vectorisation reports, inlining and LTO
**Goal:** get compiler optimisation across boundaries.
```bash
gfortran -O3 -fopt-info-vec-optimized -fopt-info-vec-missed -c kernel.f90
gfortran -O3 -flto -o app *.f90
```
- `-fopt-info-vec-missed` is equivalent to `-fopt-info-missed-vec`; the `optimized` group prints the source location of successfully vectorised loops and `missed` prints information about missed optimisations.
- `-flto` enables link-time optimisation.
- `!GCC$ ivdep` tells the compiler to ignore vector dependencies in the immediately following `DO` loop; it applies only to that loop and is implicit for `DO CONCURRENT`. The manual recommends considering OpenMP SIMD directives for new code.
- `-ffast-math` includes `-ffinite-math-only` and `-funsafe-math-optimizations`, which can change numerical results.
## Self-check
Verify the hot loop is reported as vectorised after the change.

## Checked
2026-11-02. Confirmed in the GCC manual (-fopt-info groups, -fopt-info-vec-missed equivalence, -flto, -ffast-math contents) and gfortran.texi (IVDEP directive text). Removed: -march=native in the example, reasons-list (aliasing, calls), inlining and pointer/allocatable no-alias claims, do concurrent/pure independence claim.
Method: documentation only; no commands were run.
