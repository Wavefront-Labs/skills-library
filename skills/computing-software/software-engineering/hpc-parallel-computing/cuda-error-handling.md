---
id: computing-software.software-engineering.hpc-parallel-computing.cuda-error-handling
name: cuda-error-handling
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, cuda-error-check, cuda-memcheck, compute-sanitizer, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Robustness"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Error handling and debugging

Goal: catch faults early.
- Wrap runtime calls in a check macro; kernel launches are async so errors surface later.
- `compute-sanitizer --tool memcheck|racecheck|synccheck ./app`.
- `cuda-gdb` for device debugging; `CUDA_LAUNCH_BLOCKING=1` serialises.
Verify: sanitizer clean.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
