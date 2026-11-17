---
id: computing-software.software-engineering.hpc-parallel-computing.thrust-cub-and-fft
name: thrust-cub-and-fft
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, thrust, cub, cufft, cusparse, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Algorithms"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Thrust, CUB and cuFFT

Goal: use parallel primitives.
- `thrust::sort`, `reduce`, `transform`; CUB for block/warp-level primitives and device-wide scans.
- cuFFT plans reused (`cufftPlan1d`), cuSPARSE for sparse matrices.
- Prefer library calls over custom kernels first.
Verify: output equals serial reference.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
