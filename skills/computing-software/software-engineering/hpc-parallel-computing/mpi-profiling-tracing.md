---
id: computing-software.software-engineering.hpc-parallel-computing.mpi-profiling-tracing
name: mpi-profiling-tracing
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpip, tau-profiling, vtune-mpi, ittrace, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Performance analysis"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Profiling and tracing MPI

Goal: find communication bottlenecks.
- mpiP (lightweight), TAU, Score-P/Scalasca, Extrae/Paraver, Intel APS.
- Look at time in MPI vs compute, load imbalance, message sizes.
- Roofline analysis for the compute side.
Verify: top MPI calls and imbalance identified.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
