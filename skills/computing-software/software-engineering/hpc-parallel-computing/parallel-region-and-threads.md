---
id: computing-software.software-engineering.hpc-parallel-computing.parallel-region-and-threads
name: parallel-region-and-threads
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, omp-num-threads, omp-get-thread-num, omp-proc-bind, openmp, omp-parallel, omp-threads, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Fork-join"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parallel regions and thread control

Goal: control threading.
- `#pragma omp parallel num_threads(8)`; env `OMP_NUM_THREADS`, `OMP_PROC_BIND=close`, `OMP_PLACES=cores`.
- Thread count defaults to available cores; under Slurm set it from `--cpus-per-task`.
- Nested parallelism is off by default.
Verify: `omp_get_num_threads()` reports expected value.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
