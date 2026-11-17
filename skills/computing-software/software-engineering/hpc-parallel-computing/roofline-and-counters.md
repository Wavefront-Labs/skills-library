---
id: computing-software.software-engineering.hpc-parallel-computing.roofline-and-counters
name: roofline-and-counters
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, roofline-model, perf-counters, likwid, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Performance bounds"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Roofline model and hardware counters

Goal: tell memory-bound from compute-bound.
- Arithmetic intensity (FLOP/byte) vs peak FLOPs and bandwidth; tools: Intel Advisor, Nsight Compute, LIKWID, `perf stat`.
- Optimise memory access first for low-intensity kernels.
- Benchmark peaks with STREAM and DGEMM.
Verify: kernel placed on the roofline with a plan.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
