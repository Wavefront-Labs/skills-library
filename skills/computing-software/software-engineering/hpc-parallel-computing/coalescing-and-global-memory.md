---
id: computing-software.software-engineering.hpc-parallel-computing.coalescing-and-global-memory
name: coalescing-and-global-memory
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, memory-coalescing, cudamalloc, cudamemcpy, cuda-memory, global-memory, shared-memory, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Bandwidth"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Coalesced global access

Goal: use memory bandwidth well.
- Threads in a warp should access consecutive addresses; AoS to SoA conversion.
- `cudaMalloc`, `cudaMemcpy`, pinned host memory (`cudaMallocHost`) for faster transfers.
- Measure achieved vs peak bandwidth (Nsight Compute).
Verify: global load efficiency near 100%.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
