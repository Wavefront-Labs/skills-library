---
id: computing-software.software-engineering.fortran.offload-do-concurrent
name: offload-do-concurrent
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, offload-do-concurrent, fortran-gpu]
level: sme
status: draft
description: "Offload with !$omp target teams distribute parallel do or standard parallelism via nvfortran -stdpar and flang options."
sources:
  - https://www.openacc.org/specification
  - https://www.openmp.org/specifications/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OpenMP target and do concurrent offload
**Goal:** choose a portable offload route.
```fortran
!$omp target teams distribute parallel do map(to: a, b) map(from: c)
do i = 1, n
  c(i) = a(i) + b(i)
end do
```
- `nvfortran -stdpar=gpu` offloads `do concurrent` loops to NVIDIA GPUs (compiler-specific).
- LLVM Flang and Intel ifx support OpenMP offload (`-fopenmp-targets=...`, `-fopenmp-targets=spir64` for Intel; verify flags in the current docs).
- Standard `do concurrent` is the most portable route but needs compiler support.
## Gotchas
- Offload flags change per vendor and release; unconfirmed here, check the compiler manual.
- Data movement must be explicit with `map` or managed memory.
## Self-check
Run on the host first with the directive ignored, then on the device, and compare.
