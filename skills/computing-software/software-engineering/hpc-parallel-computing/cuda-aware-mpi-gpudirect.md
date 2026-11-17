---
id: computing-software.software-engineering.hpc-parallel-computing.cuda-aware-mpi-gpudirect
name: cuda-aware-mpi-gpudirect
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, gpudirect-rdma, cuda-aware-mpi, device-pointers, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Direct GPU transfers"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CUDA-aware MPI and GPUDirect RDMA

Goal: pass device pointers to MPI.
- CUDA-aware MPI accepts `cudaMalloc` buffers in `MPI_Send`; needs UCX/`--mca pml ucx` and GPUDirect RDMA drivers (confirm).
- Bind one GPU per rank (`CUDA_VISIBLE_DEVICES` or `cudaSetDevice(local_rank)`).
- Verify with OSU micro-benchmarks.
Verify: device-to-device latency lower than staged copies.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
