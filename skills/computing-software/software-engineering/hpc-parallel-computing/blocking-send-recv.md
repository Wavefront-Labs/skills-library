---
id: computing-software.software-engineering.hpc-parallel-computing.blocking-send-recv
name: blocking-send-recv
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-send, mpi-recv, mpi-deadlock, mpi, mpi-send-recv, mpi-nonblocking, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Modes and deadlocks"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Blocking send and receive semantics

Goal: write correct two-sided communication.
- `MPI_Send(buf,count,type,dest,tag,comm)` may block until matched (eager threshold vs rendezvous); `MPI_Ssend` is always synchronous.
- Classic deadlock: two ranks both `Send` first. Fix with `MPI_Sendrecv`, ordering by rank parity or nonblocking calls.
- Match source/tag/comm; use `MPI_ANY_SOURCE` sparingly; inspect `MPI_Status`.
Verify: a ring exchange completes for sizes above the eager limit.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
