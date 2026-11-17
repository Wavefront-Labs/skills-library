---
id: computing-software.software-engineering.hpc-parallel-computing.petsc-and-fftw
name: petsc-and-fftw
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, petsc-ksp, fftw-mpi, trilinos, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Parallel solvers"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PETSc and FFTW

Goal: use parallel solver frameworks.
- PETSc: `KSPCreate`, runtime options `-ksp_type gmres -pc_type gamg -ksp_monitor`.
- FFTW-MPI for distributed FFTs; plan flags `FFTW_MEASURE`.
- Prefer libraries over custom solvers.
Verify: convergence history sane and scales.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
