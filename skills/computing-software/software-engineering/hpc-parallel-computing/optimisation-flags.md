---
id: computing-software.software-engineering.hpc-parallel-computing.optimisation-flags
name: optimisation-flags
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, march-native, fast-math, fopenmp, compiler-flags-hpc, vectorization-flags, lto, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Building fast code"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Optimisation and architecture flags

Goal: compile for the hardware.
- GCC/Clang `-O3 -march=native -fopenmp`; Intel `-xHost`; NVHPC `-fast -mp`.
- `-ffast-math` breaks IEEE semantics; use deliberately.
- Cross-compile on login nodes for compute-node ISA carefully (`-march=znver3` etc.).
Verify: same results within tolerance and faster.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
