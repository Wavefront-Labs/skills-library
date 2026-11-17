---
id: computing-software.software-engineering.hpc-parallel-computing.tasks-and-dependencies
name: tasks-and-dependencies
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, omp-task-depend, omp-taskwait, omp-taskgroup, omp-task, omp-taskloop, omp-depend, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Irregular parallelism"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tasks and dependencies

Goal: parallelise recursion and graphs.
- `#pragma omp task depend(in:a) depend(out:b)`; `taskwait`, `taskgroup`.
- Create tasks from a single thread in a `single` region; cutoff granularity (`if`, `final`) to limit overhead.
- `taskloop` splits loops into tasks.
Verify: speedup over serial recursion with a depth cutoff.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
