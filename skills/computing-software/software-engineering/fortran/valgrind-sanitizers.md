---
id: computing-software.software-engineering.fortran.valgrind-sanitizers
name: valgrind-sanitizers
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, valgrind-sanitizers, fortran-debugging]
level: advanced
status: draft
description: "Detect memory errors with valgrind and gfortran -fsanitize=address,undefined."
sources:
  - https://gcc.gnu.org/onlinedocs/gfortran/
  - https://sourceware.org/gdb/documentation/
  - https://valgrind.org/docs/manual/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Valgrind and sanitizers
**Goal:** find memory bugs.
```bash
gfortran -g -O1 -fsanitize=address,undefined -fno-omit-frame-pointer -o app_san *.f90
./app_san
gfortran -g -O0 -o app main.f90 && valgrind --leak-check=full ./app
```
- AddressSanitizer detects heap/stack overflows and use-after-free; UBSan detects undefined behaviour (limited for Fortran).
- Valgrind detects uninitialised reads, invalid accesses and leaks; slow (10-50x).
- Combine with `-fcheck=bounds` for Fortran-level array bound reports.
- Library suppressions may be needed for MPI/OpenMP runtimes.
## Gotchas
- ASan and valgrind cannot be combined in one run.
- Fortran allocatable semantics produce legitimate-looking "still reachable" blocks at exit.
## Self-check
Write one element past a heap array and confirm ASan or valgrind reports it.
