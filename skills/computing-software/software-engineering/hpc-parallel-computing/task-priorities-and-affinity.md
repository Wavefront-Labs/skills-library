---
id: computing-software.software-engineering.hpc-parallel-computing.task-priorities-and-affinity
name: task-priorities-and-affinity
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, omp-task-priority, omp-detach, omp-affinity, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Advanced tasking"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Task priorities and detach

Goal: tune tasking.
- `priority(n)` hints (needs `OMP_MAX_TASK_PRIORITY`), `detach(event)` for async completion.
- Task affinity hints are implementation-defined.
- Profile with OMPT-based tools.
Verify: critical path tasks run earlier in a trace.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
