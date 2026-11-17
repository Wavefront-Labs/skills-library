---
id: computing-software.software-engineering.fortran.openmp-reductions
name: openmp-reductions
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, openmp-reductions, fortran-openmp]
level: advanced
status: draft
description: "Reduce with reduction(+:sum) and combine with simd and collapse for vectorised parallel loops."
sources:
  - https://www.openmp.org/specifications/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OpenMP reductions and SIMD
**Goal:** parallel sums and extrema.
```fortran
!$omp parallel do reduction(+:total) reduction(max:peak)
do i = 1, n
  total = total + a(i)
  peak = max(peak, a(i))
end do
!$omp simd
do i = 1, n
  c(i) = a(i) * b(i)
end do
```
- Reduction variables get a private copy initialised to the identity and combined at the end.
- Operators: `+ * - .and. .or. .eqv. .neqv. max min iand ior ieor`.
- Floating-point results vary with thread count due to association order.
## Gotchas
- Reduction on array sections needs OpenMP 4.5+ syntax and compiler support.
- Combine `target` offload only with compilers built for it (gfortran offload is installation-specific).
## Self-check
Compare the parallel sum against a serial sum within tolerance.
