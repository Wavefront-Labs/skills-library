---
id: computing-software.software-engineering.hpc-parallel-computing.mpi-io-collective-writes
name: mpi-io-collective-writes
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-file-open, mpi-file-set-view, collective-buffering, mpi-io, mpi-file-write-all, hdf5-parallel, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "File views"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MPI-IO collective I/O

Goal: write one file from many ranks.
- `MPI_File_set_view` with subarray types, then `MPI_File_write_at_all` for collective buffering.
- Align to filesystem stripe size; use hints (`romio_cb_write`, `striping_factor`).
- Avoid file-per-process at scale (metadata storm).
Verify: file bytes equal serial reference.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
