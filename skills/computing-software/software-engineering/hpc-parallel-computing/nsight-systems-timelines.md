---
id: computing-software.software-engineering.hpc-parallel-computing.nsight-systems-timelines
name: nsight-systems-timelines
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, nsys-profile, gpu-timeline, nvtx-ranges, nsight-systems, nsight-compute, rocprof, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "System-level profiling"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nsight Systems timelines

Goal: find gaps and overlaps.
- `nsys profile -o out --trace=cuda,nvtx,mpi ./app`; open in the GUI or `nsys stats`.
- Add NVTX ranges to label phases.
- Look for idle GPU, sync stalls, small kernels.
Verify: timeline reveals the largest gap.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
