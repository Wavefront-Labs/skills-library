---
id: computing-software.software-engineering.fortran.mpi-communication
name: mpi-communication
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, mpi-communication, fortran-mpi]
level: advanced
status: draft
description: "Exchange data with MPI_Send/Recv, nonblocking calls and MPI_Allreduce, MPI_Bcast and halo exchanges."
sources:
  - https://www.mpi-forum.org/docs/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MPI point-to-point and collectives
**Goal:** communicate between ranks.
```fortran
call MPI_Send(buf, n, MPI_DOUBLE_PRECISION, dest, tag, MPI_COMM_WORLD)
call MPI_Recv(buf, n, MPI_DOUBLE_PRECISION, src, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE)
call MPI_Allreduce(MPI_IN_PLACE, total, 1, MPI_DOUBLE_PRECISION, MPI_SUM, MPI_COMM_WORLD)
call MPI_Isend(buf, n, MPI_DOUBLE_PRECISION, dest, tag, MPI_COMM_WORLD, req)
call MPI_Wait(req, MPI_STATUS_IGNORE)
```
- Blocking send/receive pairs can deadlock; use `MPI_Sendrecv` or nonblocking calls for halo exchange.
- Collectives (`MPI_Bcast`, `MPI_Reduce`, `MPI_Gather`, `MPI_Scatter`) involve all ranks of the communicator.
- Datatype constants must match the Fortran kind (`real(dp)` with `MPI_DOUBLE_PRECISION`).
- Passing array sections can force temporary copies with nonblocking calls; use contiguous buffers.
## Gotchas
- Nonblocking calls require the buffer to stay unmodified until completion.
- Mismatched tags or counts hang the job.
## Self-check
Ring-pass a value around all ranks and verify the sum with `MPI_Allreduce`.
