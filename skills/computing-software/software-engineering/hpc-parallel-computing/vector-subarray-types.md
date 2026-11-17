---
id: computing-software.software-engineering.hpc-parallel-computing.vector-subarray-types
name: vector-subarray-types
category: computing-software
field: software-engineering
product: hpc-parallel-computing
tags: [hpc-parallel-computing, mpi-type-vector, mpi-type-create-subarray, mpi-type-commit, mpi-datatypes, mpi-pack, hpc, parallel-programming, supercomputing]
level: practitioner
status: draft
description: "Non-contiguous data"
sources: ["https://www.mpi-forum.org/docs/", "https://www.openmp.org/specifications/", "https://slurm.schedmd.com/documentation.html", "https://docs.nvidia.com/cuda/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vector and subarray datatypes

Goal: send strided data without copying.
- `MPI_Type_vector(count,blocklen,stride,old,&new)`, `MPI_Type_create_subarray` for N-d slices, then `MPI_Type_commit`/`Type_free`.
- Halo exchange of columns is the classic use.
- Derived types may be slower than manual pack for tiny messages (measure).
Verify: received data matches expected strided pattern.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
