---
id: computing-software.software-engineering.hpc-parallel-computing.hybrid-layout-tuning
name: hybrid-layout-tuning
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, ranks-per-node, threads-per-rank, numa-domain-per-rank, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Layout"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rank and thread layout

Goal: choose ranks x threads.
- Typical: one rank per NUMA domain or L3 cache, threads fill the domain.
- Slurm: `--ntasks-per-node=4 --cpus-per-task=16` with `OMP_NUM_THREADS=16`.
- Benchmark several layouts.
Verify: best layout identified by time per step.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
