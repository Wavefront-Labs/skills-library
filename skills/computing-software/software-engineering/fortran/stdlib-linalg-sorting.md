---
id: computing-software.software-engineering.fortran.stdlib-linalg-sorting
name: stdlib-linalg-sorting
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, stdlib-linalg-sorting, fortran-stdlib]
level: advanced
status: draft
description: "Call stdlib_linalg, stdlib_sorting and stdlib_stats wrappers for common numeric operations, checking the docs for current signatures."
sources:
  - https://stdlib.fortran-lang.org/
  - https://fpm.fortran-lang.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# stdlib linear algebra, sorting and statistics
**Goal:** reuse numerical routines.
- `stdlib_sorting`: `sort(array)`, `sort_index(array, index)`, `ord_sort`, `radix_sort`.
```fortran
use stdlib_sorting, only: sort
real :: v(5) = [3., 1., 4., 1., 5.]
call sort(v)                       ! ascending in place (check optional 'reverse' argument)
```
- `stdlib_stats`: `mean`, `median`, `var` (with `dim` and `mask` options).
- `stdlib_linalg`: `eye`, `diag`, `trace`, `det`, `inv`, `solve`, `lstsq`, `svd`, `eig` wrappers over LAPACK (availability depends on version; unconfirmed per release).
- Requires BLAS/LAPACK at link time for linalg routines.
## Gotchas
- Function signatures differ between stdlib versions; consult docs for your version.
- Sorting stability and algorithm differ per routine (`ord_sort` is stable merge-style; verify in docs).
## Self-check
Sort a small array and compare with a hand-sorted answer.
