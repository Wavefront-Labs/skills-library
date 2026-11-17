---
id: computing-software.software-engineering.fortran.blas-lapack-calls
name: blas-lapack-calls
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, blas-lapack-calls, fortran-blas-lapack]
level: practitioner
status: draft
description: "Call dgemm, dgemv and dgesv with correct arguments, leading dimensions and info checks."
sources:
  - https://gcc.gnu.org/onlinedocs/gfortran/
  - https://cmake.org/cmake/help/latest/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calling BLAS and LAPACK from Fortran
**Goal:** use optimised linear algebra.
```fortran
external :: dgemm, dgesv
! C = alpha*A*B + beta*C
call dgemm('N', 'N', m, n, k, 1.0d0, a, m, b, k, 0.0d0, c, m)
integer :: ipiv(n), info
call dgesv(n, 1, a, n, ipiv, x, n, info)   ! solve A x = b, b overwritten by x
if (info /= 0) error stop 'dgesv failed'
```
- Routine names: leading letter s/d/c/z = precision; leading dimension `lda` >= rows.
- Arrays are column-major, matching Fortran.
- `a` is overwritten by the LU factors; copy first if needed.
- Declare `external` or use explicit interfaces from a module (e.g. `stdlib_linalg_blas`) for argument checks (unconfirmed module availability).
## Gotchas
- Passing integers of the wrong kind with ILP64 builds (MKL ilp64, OpenBLAS ILP64) corrupts calls.
- For small matrices, `matmul` may be faster than library overhead; large ones need BLAS (`-fexternal-blas` can redirect `matmul`).
## Self-check
Solve a 3x3 system with `dgesv` and check `a*x - b` is near zero.
