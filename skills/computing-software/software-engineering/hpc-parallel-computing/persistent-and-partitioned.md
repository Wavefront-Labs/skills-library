---
id: computing-software.software-engineering.hpc-parallel-computing.persistent-and-partitioned
name: persistent-and-partitioned
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-psend-init, partitioned-communication, mpi-start, mpi-persistent, mpi-partitioned, mpi-sessions, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "MPI 4 features"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Persistent and partitioned communication

Goal: reduce overhead for repeated patterns.
- Persistent collectives/point-to-point: initialise once, `MPI_Start` per iteration.
- Partitioned communication (`MPI_Psend_init`, `MPI_Pready`) lets threads/GPU kernels mark buffer parts ready (MPI 4.0; confirm library support).
- Compare against plain nonblocking calls.
Verify: lower per-iteration time on repeated halos.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
