---
id: computing-software.software-engineering.hpc-parallel-computing.blas-lapack-tuned
name: blas-lapack-tuned
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, openblas, mkl, blis, blas-lapack, scalapack, petsc, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Dense linear algebra"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BLAS/LAPACK implementations

Goal: link a fast BLAS.
- OpenBLAS, MKL, BLIS, vendor BLAS; control threads (`OMP_NUM_THREADS`/`MKL_NUM_THREADS`).
- Avoid oversubscription when nesting threaded BLAS in MPI/OpenMP.
- Verify with a DGEMM benchmark.
Verify: GFLOP/s near peak.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
