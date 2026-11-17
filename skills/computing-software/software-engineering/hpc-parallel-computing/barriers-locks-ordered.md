---
id: computing-software.software-engineering.hpc-parallel-computing.barriers-locks-ordered
name: barriers-locks-ordered
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, omp-lock, omp-ordered, omp-master, omp-barrier, omp-flush, omp-locks, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Synchronisation"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Barriers, locks and ordered

Goal: synchronise correctly.
- `barrier`, `master/masked`, `single`, `ordered`, `omp_set_lock`.
- Excess barriers cost; `nowait` where safe.
- Prefer lock-free reductions.
Verify: no deadlocks; output order correct where required.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
