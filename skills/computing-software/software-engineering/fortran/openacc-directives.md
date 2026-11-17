---
id: computing-software.software-engineering.fortran.openacc-directives
name: openacc-directives
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, openacc-directives, fortran-gpu]
level: advanced
status: draft
description: "Offload loops with !$acc parallel loop, data regions and the vendor compiler flags."
sources:
  - https://www.openacc.org/specification
  - https://www.openmp.org/specifications/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OpenACC directives
**Goal:** offload loops to a GPU.
```fortran
!$acc data copyin(a, b) copyout(c)
!$acc parallel loop
do i = 1, n
  c(i) = a(i) + b(i)
end do
!$acc end data
```
- Compile with an OpenACC-capable compiler, e.g. NVIDIA `nvfortran -acc` (or recent GCC with `-fopenacc`, with offload support as built).
- Data clauses: `copy`, `copyin`, `copyout`, `create`, `present`.
- Keep data on the device across kernels with `!$acc data` regions to avoid transfers.
## Gotchas
- Offload support depends on how the compiler was built and installed; check `-fopenacc` support in your distribution.
- Transfers dominate small kernels.
## Self-check
Compare results with the CPU version and check timing with larger arrays.
