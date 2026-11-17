---
id: computing-software.software-engineering.hpc-parallel-computing.nonblocking-and-overlap
name: nonblocking-and-overlap
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-isend, mpi-irecv, mpi-wait, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Overlapping compute and comms"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nonblocking communication and overlap

Goal: hide latency.
- `MPI_Isend/Irecv` then `MPI_Waitall`; do not touch buffers until completion; use `MPI_Test` to poll.
- Progress may only happen inside MPI calls; poke with `MPI_Test` or use async progress (implementation-specific, confirm).
- Persistent requests (`MPI_Send_init`, `MPI_Start`) cut setup cost in loops.
Verify: time with and without overlap shows a gain.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
