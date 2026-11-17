---
id: computing-software.software-engineering.hpc-parallel-computing.omp-target-offload
name: omp-target-offload
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, omp-target-teams, omp-map-clause, omp-target-data, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Accelerators"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Target offload to GPUs

Goal: offload loops.
- `#pragma omp target teams distribute parallel for map(to:a[0:n]) map(from:b[0:n])`.
- `target data` keeps arrays resident across kernels; `target enter/exit data`.
- Compiler/runtime support varies (nvc, clang, gcc, ROCm, oneAPI - confirm).
Verify: profile shows kernels and data movement as designed.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
