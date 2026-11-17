---
id: computing-software.software-engineering.hpc-parallel-computing.mpi-implementation-choice
name: mpi-implementation-choice
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, openmpi, mpich, intel-mpi, cray-mpich, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Implementation differences"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Open MPI, MPICH and vendor MPIs

Goal: pick and tune an MPI.
- Open MPI uses MCA parameters (`--mca btl ...`, `--mca pml ucx`); MPICH uses CH4 with OFI/UCX.
- Use the site-provided MPI tied to the interconnect.
- Compile and run with the same MPI; check `mpicc --showme`.
Verify: `ompi_info` or `mpichversion` matches the build.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
