---
id: computing-software.software-engineering.hpc-parallel-computing.application-checkpoints
name: application-checkpoints
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, checkpoint-restart, restart-files, checkpoint-frequency, dmtcp, fault-tolerance, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Surviving failures"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Application-level checkpointing

Goal: make long runs restartable.
- Write state periodically (HDF5/ADIOS); choose interval via Young/Daly: sqrt(2 * checkpoint_cost * MTBF).
- Write to a temp name then rename atomically; keep two generations.
- Test restart equality.
Verify: restarted run reproduces results.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
