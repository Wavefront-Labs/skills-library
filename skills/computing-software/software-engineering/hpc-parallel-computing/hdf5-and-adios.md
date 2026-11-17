---
id: computing-software.software-engineering.hpc-parallel-computing.hdf5-and-adios
name: hdf5-and-adios
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, parallel-hdf5, adios2, netcdf-parallel, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "High-level I/O libraries"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HDF5 and ADIOS2

Goal: use portable self-describing formats.
- Parallel HDF5: `H5Pset_fapl_mpio`, collective dataset transfer property; chunking matters.
- ADIOS2 provides engines (BP5, SST for in-situ).
- Match chunk/stripe to access patterns.
Verify: read-back and h5dump match.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
