---
id: computing-software.software-engineering.hpc-parallel-computing.comm-split-and-groups
name: comm-split-and-groups
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-comm-split, mpi-comm-dup, mpi-group, mpi-communicators, mpi-cartesian, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Subcommunicators"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Splitting communicators

Goal: build row/column or node-local communicators.
- `MPI_Comm_split(comm, color, key, &new)`; `MPI_Comm_split_type(..., MPI_COMM_TYPE_SHARED, ...)` for node-local.
- Free communicators with `MPI_Comm_free`; leaks hurt at scale.
- Use `MPI_Comm_dup` for library isolation.
Verify: rank/size in each subcommunicator is as designed.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
