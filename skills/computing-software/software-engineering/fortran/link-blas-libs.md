---
id: computing-software.software-engineering.fortran.link-blas-libs
name: link-blas-libs
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, link-blas-libs, fortran-blas-lapack]
level: practitioner
status: draft
description: "Link BLAS and LAPACK implementations with the right flags for gfortran, CMake and fpm."
sources:
  - https://gcc.gnu.org/onlinedocs/gfortran/
  - https://cmake.org/cmake/help/latest/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Linking OpenBLAS, MKL and reference BLAS
**Goal:** link numerical libraries correctly.
```bash
gfortran main.f90 -llapack -lblas              # reference libs
gfortran main.f90 -lopenblas                   # OpenBLAS (includes LAPACK)
gfortran main.f90 -L<dir> -lopenblas
```
- fpm: `[build] link = ["lapack", "blas"]` in `fpm.toml`.
- CMake: `find_package(LAPACK REQUIRED)` and link `LAPACK::LAPACK`.
- Intel MKL: use the Intel link-line advisor to choose the right interface layer (LP64 vs ILP64) and threading.
- Control threading with `OPENBLAS_NUM_THREADS` or `MKL_NUM_THREADS`.
## Gotchas
- Mixing threaded BLAS with OpenMP loops oversubscribes cores.
- Link order matters on some linkers: libraries after objects.
## Self-check
Run a `dgemm` and monitor core usage with the thread variable set to 1 and 4.
