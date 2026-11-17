---
id: computing-software.software-engineering.hpc-parallel-computing.numa-and-first-touch
name: numa-and-first-touch
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, numa-first-touch, omp-places, numactl, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Memory locality"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NUMA, first-touch and affinity

Goal: place data near threads.
- Pages are placed by first touch: initialise arrays in a parallel loop with the same schedule as the compute loop.
- Bind threads (`OMP_PROC_BIND=spread`) and use `numactl --interleave` for irregular access.
- Check with `numastat`.
Verify: memory bandwidth (STREAM) scales with threads.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
