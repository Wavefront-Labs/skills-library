---
id: computing-software.software-engineering.hpc-parallel-computing.loop-scheduling
name: loop-scheduling
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, omp-schedule-static, omp-schedule-dynamic, omp-schedule-guided, omp-for, omp-schedule, omp-reduction, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Load balance"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Loop scheduling

Goal: balance iterations.
- `schedule(static)` default-ish; `dynamic,chunk` for irregular work; `guided`; `runtime` with `OMP_SCHEDULE`.
- `collapse(2)` merges nested loops; `nowait` removes the implicit barrier.
- Measure; dynamic adds overhead.
Verify: thread times balanced in a profile.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
