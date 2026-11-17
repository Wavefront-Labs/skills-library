---
id: computing-software.software-engineering.hpc-parallel-computing.rma-windows-and-sync
name: rma-windows-and-sync
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-win-create, mpi-win-fence, mpi-win-lock, mpi-rma, mpi-win, mpi-put-get, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Remote memory access"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RMA windows and synchronisation

Goal: use RMA safely.
- `MPI_Win_allocate`, `MPI_Put/Get/Accumulate`, sync by `MPI_Win_fence`, PSCW, or `MPI_Win_lock_all/flush`.
- Data races within an epoch are undefined; use `MPI_Accumulate` for atomic ops.
- Performance depends heavily on the MPI and network (confirm with benchmarks).
Verify: remote counters sum correctly under contention.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
