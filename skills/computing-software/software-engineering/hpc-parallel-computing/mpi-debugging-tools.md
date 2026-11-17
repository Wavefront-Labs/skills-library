---
id: computing-software.software-engineering.hpc-parallel-computing.mpi-debugging-tools
name: mpi-debugging-tools
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-deadlock-debug, parallel-debugger, valgrind-mpi, mpi-debugging, mpi-profiling, scalasca, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Finding bugs"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debugging MPI programs

Goal: debug parallel failures.
- Print rank in logs; run small (`-np 2`); use `gdb` attach per rank or parallel debuggers (DDT, TotalView).
- MUST (MPI correctness checker) finds type/buffer mismatches (confirm availability).
- Core dumps per rank may swamp the file system.
Verify: bug reproduces at small scale and is fixed.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
