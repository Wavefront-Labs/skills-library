---
id: computing-software.software-engineering.hpc-parallel-computing.mpi-thread-levels
name: mpi-thread-levels
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-thread-funneled, mpi-thread-serialized, thread-safety, hybrid-mpi-openmp, mpi-thread-multiple, mpi-init-thread, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "MPI_Init_thread"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MPI thread support levels

Goal: mix MPI and threads safely.
- `MPI_Init_thread(&argc,&argv,MPI_THREAD_FUNNELED,&provided)`; check `provided`.
- FUNNELED: only the main thread calls MPI; MULTIPLE needs a thread-safe build and may be slower.
- Do MPI outside parallel regions when possible.
Verify: `provided` equals the requested level.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
