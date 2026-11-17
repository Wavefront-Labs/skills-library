---
id: computing-software.software-engineering.hpc-parallel-computing.data-sharing-clauses
name: data-sharing-clauses
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, omp-private, omp-firstprivate, omp-shared, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Variable scope"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data-sharing clauses

Goal: avoid races.
- `default(none)` forces explicit scoping; `private`, `firstprivate`, `lastprivate`, `shared`, `reduction`.
- Loop variables are private; globals are shared by default.
- Use `threadprivate` for static state.
Verify: runs with Helgrind/TSan or Archer show no races.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
