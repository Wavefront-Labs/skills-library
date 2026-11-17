---
id: computing-software.software-engineering.hpc-parallel-computing.cartesian-topologies
name: cartesian-topologies
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-cart-create, mpi-cart-shift, mpi-dims-create, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Domain decomposition"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cartesian and graph topologies

Goal: map ranks to a grid.
- `MPI_Dims_create`, `MPI_Cart_create(comm,ndims,dims,periods,reorder,&cart)`, `MPI_Cart_shift` for neighbours.
- `reorder=1` lets MPI map to hardware.
- Neighbour collectives (`MPI_Neighbor_alltoall`) for halo exchange.
Verify: neighbours of corner ranks are `MPI_PROC_NULL` when non-periodic.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
