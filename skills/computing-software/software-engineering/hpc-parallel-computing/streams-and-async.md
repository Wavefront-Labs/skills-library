---
id: computing-software.software-engineering.hpc-parallel-computing.streams-and-async
name: streams-and-async
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, cuda-stream, cuda-event, memcpy-async, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Overlap"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Streams, events and async copies

Goal: overlap copies and kernels.
- Use pinned memory and `cudaMemcpyAsync` on multiple streams; `cudaEventRecord` for timing.
- Default stream sync behaviour: use per-thread default stream (`--default-stream per-thread`) if needed.
- CUDA graphs reduce launch overhead for repeated work.
Verify: Nsight Systems shows overlapped timelines.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
