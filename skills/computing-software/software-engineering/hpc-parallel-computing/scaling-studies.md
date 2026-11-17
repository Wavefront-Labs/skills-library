---
id: computing-software.software-engineering.hpc-parallel-computing.scaling-studies
name: scaling-studies
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, strong-scaling, weak-scaling, amdahl, roofline, profiling-hpc, amdahl-law, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Measuring scalability"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Strong and weak scaling

Goal: quantify parallel efficiency.
- Strong: fixed problem, vary cores; efficiency = T1/(N*TN). Weak: fixed work per core.
- Amdahl's law limits speedup by serial fraction; plot speedup and efficiency.
- Repeat runs; control noise (exclusive nodes).
Verify: scaling plot with error bars and stated efficiency.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
