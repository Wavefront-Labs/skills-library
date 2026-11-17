---
id: computing-software.software-engineering.hpc-parallel-computing.kernel-launch-and-indexing
name: kernel-launch-and-indexing
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, cuda-kernel-launch, threadidx, grid-stride-loop, cuda, cuda-kernel, thread-hierarchy, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Writing kernels"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Kernels, grids and indexing

Goal: write a correct kernel.
- `__global__ void f(float* a,int n){int i=blockIdx.x*blockDim.x+threadIdx.x; if(i<n) a[i]*=2;}` launched `f<<<(n+255)/256,256>>>(a,n)`.
- Grid-stride loops decouple grid size from n.
- Always check launch errors: `cudaGetLastError()` and `cudaDeviceSynchronize()`.
Verify: results match CPU reference.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
