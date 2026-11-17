---
id: computing-software.software-engineering.hpc-parallel-computing.hip-and-rocm
name: hip-and-rocm
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, hip-programming, hipify, rocm, kokkos, sycl, hip, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "AMD GPUs"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HIP and ROCm

Goal: write portable GPU code.
- HIP mirrors CUDA APIs (`hipMalloc`, `hipLaunchKernelGGL`); convert with `hipify-perl`.
- Build with `hipcc`; profile with `rocprof`.
- Behavioural differences (warp size 64 on some GPUs) need care.
Verify: results match on both vendors.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
