---
id: computing-software.software-engineering.hpc-parallel-computing.shared-memory-windows
name: shared-memory-windows
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-win-allocate-shared, mpi-win-shared-query, node-local-shared, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Intra-node sharing"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shared-memory windows

Goal: share memory among ranks on a node.
- `MPI_Win_allocate_shared` on a shared communicator, then `MPI_Win_shared_query` for pointers.
- Reduces memory duplication for read-only tables.
- Synchronise with `MPI_Win_sync` and barriers.
Verify: memory per node falls versus replicated arrays.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
