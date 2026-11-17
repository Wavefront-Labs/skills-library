---
id: computing-software.software-engineering.fortran.openmp-data-sharing
name: openmp-data-sharing
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, openmp-data-sharing, fortran-openmp]
level: advanced
status: draft
description: "Use default(none), private, firstprivate, shared and critical/atomic to avoid races."
sources:
  - https://www.openmp.org/specifications/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OpenMP data sharing and races
**Goal:** write race-free parallel regions.
```fortran
!$omp parallel do default(none) shared(a, b, n) private(i)
do i = 1, n
  a(i) = a(i) + b(i)
end do
!$omp atomic
count = count + 1
```
- Loop index is private automatically.
- `firstprivate(x)` copies the initial value; `lastprivate(x)` copies the last iteration's.
- Use `critical` for blocks and `atomic` for single updates.
- Implicit-save variables and module variables are shared; allocate per-thread arrays inside the region.
- gfortran thread-safety: procedures called in parallel need `recursive` or `-frecursive` (implied by `-fopenmp`).
## Gotchas
- Calling non-thread-safe I/O or random number routines concurrently is unsafe.
- `default(none)` surfaces forgotten variables at compile time.
## Self-check
Remove `atomic` and observe an incorrect count under multiple threads.
