---
id: computing-software.software-engineering.hpc-parallel-computing.struct-types-and-pack
name: struct-types-and-pack
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-type-create-struct, mpi-pack-unpack, mpi-get-address, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Heterogeneous data"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Struct types and MPI_Pack

Goal: send structs.
- `MPI_Type_create_struct` with `MPI_Get_address` displacements; resize extent for arrays of structs (`MPI_Type_create_resized`).
- `MPI_Pack/Unpack` for dynamic layout.
- Avoid sending padding assumptions across architectures.
Verify: array of structs round-trips.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
