---
id: computing-software.software-engineering.hpc-parallel-computing.fortran-and-c-interop
name: fortran-and-c-interop
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, iso-c-binding, fortran-mpi, mixed-language, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Mixed-language builds"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fortran/C interop in HPC

Goal: link legacy codes.
- Use `bind(C)` and `iso_c_binding`; name mangling trailing underscores otherwise.
- `mpif90` / `mpifort` and `use mpi_f08` module.
- Match compilers across languages.
Verify: link succeeds and calls return correct data.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
