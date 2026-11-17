---
id: computing-software.software-engineering.fortran.mpi-f08
name: mpi-f08
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, mpi-f08, fortran-mpi]
level: practitioner
status: draft
description: "Initialise MPI, query rank and size, finalise, and compile with mpifort using the use mpi_f08 bindings."
sources:
  - https://www.mpi-forum.org/docs/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MPI with the mpi_f08 module
**Goal:** write a minimal MPI program.
```fortran
program hello
  use mpi_f08
  implicit none
  integer :: rank, nprocs
  call MPI_Init()
  call MPI_Comm_rank(MPI_COMM_WORLD, rank)
  call MPI_Comm_size(MPI_COMM_WORLD, nprocs)
  print *, 'rank', rank, 'of', nprocs
  call MPI_Finalize()
end program
```
```bash
mpifort -o hello hello.f90 && mpirun -n 4 ./hello
```
- `mpi_f08` (MPI-3) gives type-checked handles (`type(MPI_Comm)`) and optional `ierror`.
- Older codes use `use mpi` or `include 'mpif.h'` with explicit `ierror` argument.
## Gotchas
- The MPI module must be built with the same compiler as your code (module compatibility).
- Output ordering across ranks is nondeterministic.
## Self-check
Run with 4 ranks and confirm four lines.
