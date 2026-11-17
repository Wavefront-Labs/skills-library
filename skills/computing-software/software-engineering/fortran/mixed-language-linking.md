---
id: computing-software.software-engineering.fortran.mixed-language-linking
name: mixed-language-linking
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, mixed-language-linking, fortran-interop-python]
level: advanced
status: draft
description: "Link mixed-language programs, choose the linker driver, and add libgfortran when linking Fortran objects from C."
sources:
  - https://numpy.org/doc/stable/f2py/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Linking Fortran with C, C++ and runtime libraries
**Goal:** link multi-language binaries.
- Easiest: link with the Fortran driver (`gfortran main.o c_part.o -lstdc++`) so Fortran runtime libs are added automatically.
- From C: `gcc main.o ftn.o -lgfortran` (and `-lm`, plus `-lquadmath` if used).
- For C++ calling Fortran use `extern "C"` and `bind(c)` interfaces.
- Print the library list with `gfortran -v` or use CMake `FortranCInterface` to detect mangling.
- Match compilers from one vendor family to avoid ABI differences.
## Gotchas
- Mixing Intel and GNU runtimes gives duplicate I/O unit tables and strange output behaviour.
- Static linking Fortran: `-static-libgfortran` (check licence runtime exception details).
## Self-check
Link a C `main` that calls a Fortran routine and confirm it runs with no unresolved symbols.
