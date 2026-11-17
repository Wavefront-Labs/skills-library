---
id: computing-software.software-engineering.hpc-parallel-computing.shared-memory-tiling
name: shared-memory-tiling
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, shared-memory-tile, bank-conflicts, syncthreads, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Data reuse"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shared memory and tiling

Goal: reuse data on-chip.
- `__shared__ float tile[32][33];` padding avoids bank conflicts; `__syncthreads()` between load and use.
- Classic example: tiled matrix multiply.
- Shared memory size limits occupancy.
Verify: bank conflict count is zero in profiler.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
