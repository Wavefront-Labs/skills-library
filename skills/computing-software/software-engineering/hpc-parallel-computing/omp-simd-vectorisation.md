---
id: computing-software.software-engineering.hpc-parallel-computing.omp-simd-vectorisation
name: omp-simd-vectorisation
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, omp-simd-pragma, aligned-clause, safelen, omp-simd, omp-target, omp-teams, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Vectorisation"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SIMD directives

Goal: vectorise loops.
- `#pragma omp simd reduction(+:s) aligned(a:64) safelen(8)`; `declare simd` for functions.
- Check compiler reports (`-fopt-info-vec`, `-qopt-report`).
- Remove aliasing with `restrict`.
Verify: vectorised loop reported and faster.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
