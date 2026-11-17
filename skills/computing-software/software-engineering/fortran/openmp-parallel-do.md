---
id: computing-software.software-engineering.fortran.openmp-parallel-do
name: openmp-parallel-do
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, openmp-parallel-do, fortran-openmp]
level: practitioner
status: draft
description: "Parallelise loops with !$omp parallel do, schedule clauses and the -fopenmp flag."
sources:
  - https://www.openmp.org/specifications/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OpenMP parallel do and workshare
**Goal:** add shared-memory parallelism.
```fortran
!$omp parallel do schedule(static) private(tmp)
do i = 1, n
  tmp = f(a(i))
  b(i) = tmp
end do
!$omp end parallel do
```
```bash
gfortran -O2 -fopenmp -o app *.f90
OMP_NUM_THREADS=4 ./app
```
- `!$omp workshare` parallelises array assignments.
- Clauses: `schedule(static|dynamic|guided, chunk)`, `collapse(2)`, `num_threads(n)`.
- `use omp_lib` gives `omp_get_wtime`, `omp_get_thread_num`, `omp_get_max_threads`.
## Gotchas
- Without `-fopenmp`, directives are comments and the program runs serially.
- Loop iterations must be independent; shared writes cause data races.
## Self-check
Compare timing at 1 and 4 threads and verify identical results.
