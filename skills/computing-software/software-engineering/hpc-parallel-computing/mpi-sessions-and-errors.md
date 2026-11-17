---
id: computing-software.software-engineering.hpc-parallel-computing.mpi-sessions-and-errors
name: mpi-sessions-and-errors
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-session-init, mpi-errhandler, mpi-abort, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Robustness"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sessions model and error handling

Goal: handle errors and initialise flexibly.
- Sessions (`MPI_Session_init`) allow library-local initialisation without `MPI_COMM_WORLD`.
- Set `MPI_ERRORS_RETURN` to handle errors; default aborts.
- ULFM fault tolerance is an extension in some implementations (confirm).
Verify: an error code is detected and reported rather than aborting.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
