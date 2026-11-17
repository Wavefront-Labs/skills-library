---
id: computing-software.software-engineering.hpc-parallel-computing.reductions-and-broadcast
name: reductions-and-broadcast
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-reduce, mpi-bcast-tree, mpi-op, mpi-collectives, mpi-bcast, mpi-allreduce, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Common collectives"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bcast, Reduce, Allreduce

Goal: use collectives instead of hand-rolled loops.
- `MPI_Allreduce(MPI_IN_PLACE, x, n, MPI_DOUBLE, MPI_SUM, comm)`.
- All ranks must call collectives in the same order with consistent counts.
- Floating-point reductions are not bitwise reproducible across process counts.
Verify: sum matches serial within tolerance.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
