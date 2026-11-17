---
id: computing-software.software-engineering.hpc-parallel-computing.cublas-and-cusolver
name: cublas-and-cusolver
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, cublas-sgemm, cusolver, tensor-cores, cublas, cufft, thrust, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Dense linear algebra"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# cuBLAS and cuSOLVER

Goal: use vendor kernels.
- `cublasSgemm(handle, ...)` uses column-major layout; `cublasGemmEx` for mixed precision/Tensor Cores.
- Create the handle once; batched APIs for small matrices.
- Verify numerics versus CPU BLAS.
Verify: GFLOP/s near vendor peak.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
