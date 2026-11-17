---
id: computing-software.software-engineering.hpc-parallel-computing.reductions-and-atomics
name: reductions-and-atomics
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, omp-reduction-clause, omp-atomic, omp-critical, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Safe accumulation"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reductions, atomics and critical

Goal: accumulate safely.
- `reduction(+:sum)` beats `atomic` beats `critical`; user-defined reductions with `declare reduction`.
- Floating-point order changes results slightly.
- Avoid false sharing on per-thread counters: pad to cache lines.
Verify: results match serial within tolerance.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
