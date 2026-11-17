---
id: computing-software.software-engineering.hpc-parallel-computing.occupancy-and-divergence
name: occupancy-and-divergence
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, occupancy-calculator, warp-divergence, register-pressure, cuda-occupancy, cuda-streams, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Execution efficiency"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Occupancy and warp divergence

Goal: keep SMs busy.
- Occupancy = resident warps / max; limited by registers, shared memory, block size.
- Divergent branches within a warp serialise.
- `__launch_bounds__` and `-maxrregcount` control registers.
Verify: achieved occupancy and issue slot utilisation improve.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
