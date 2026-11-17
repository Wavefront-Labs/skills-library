---
id: computing-software.software-engineering.hpc-parallel-computing.scatter-gather-alltoall
name: scatter-gather-alltoall
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-scatter, mpi-gather, mpi-alltoall, mpi-allgatherv, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Data redistribution"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scatter, Gather, Alltoall

Goal: distribute and collect data.
- `MPI_Scatterv`/`Gatherv` take counts and displacements arrays.
- `Alltoall` is bandwidth-hungry: use for FFT transposes; consider `MPI_Alltoallv` for imbalance.
- Nonblocking collectives (`MPI_Iallreduce`) enable overlap.
Verify: gathered array equals expected layout.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
