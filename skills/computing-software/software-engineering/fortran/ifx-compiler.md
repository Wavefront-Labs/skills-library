---
id: computing-software.software-engineering.fortran.ifx-compiler
name: ifx-compiler
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, ifx-compiler, fortran-other-compilers]
level: practitioner
status: draft
description: "Use Intel's LLVM-based ifx (oneAPI), map common gfortran flags, and know the older ifort is discontinued."
sources:
  - https://www.intel.com/content/www/us/en/developer/tools/oneapi/fortran-compiler.html
  - https://flang.llvm.org/docs/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Intel ifx compiler
**Goal:** build with Intel Fortran.
```bash
ifx -O2 -warn all -check all -o app main.f90          # Linux
ifx /O2 /warn:all /check:all main.f90                 # Windows
ifx -qopenmp -O3 -xHost ...
```
- ifx is the LLVM-based oneAPI compiler; classic ifort has been deprecated and removed from recent oneAPI releases (check current release notes).
- Equivalents: `-check all` ~ `-fcheck=all`; `-traceback` for backtraces; `-fpe0` traps; `-xHost` ~ `-march=native`; `-warn all` ~ `-Wall`; `-qopenmp` ~ `-fopenmp`.
- Source oneAPI environment before use (`setvars` script).
## Gotchas
- `.mod` files are not compatible with gfortran's.
- Default options differ (e.g. stack arrays, realloc-lhs); check `-standard-semantics`.
## Self-check
Build the same project with gfortran and ifx and diff the outputs within tolerance.
