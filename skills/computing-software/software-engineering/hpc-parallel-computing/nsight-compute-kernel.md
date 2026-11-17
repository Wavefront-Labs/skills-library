---
id: computing-software.software-engineering.hpc-parallel-computing.nsight-compute-kernel
name: nsight-compute-kernel
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, ncu, kernel-metrics, speed-of-light, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Kernel-level profiling"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nsight Compute kernel analysis

Goal: tune a kernel.
- `ncu --set full -k kernel_name ./app`; Speed of Light, memory chart, warp state sections.
- Compare before/after with baselines.
- Profile one invocation (`-c 1`) to limit overhead.
Verify: targeted metric improves.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
