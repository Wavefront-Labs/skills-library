---
id: computing-software.software-engineering.fortran.llvm-flang
name: llvm-flang
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, llvm-flang, fortran-other-compilers]
level: practitioner
status: draft
description: "Compile with LLVM Flang (flang-new, now flang), know its feature coverage and how its flags differ."
sources:
  - https://www.intel.com/content/www/us/en/developer/tools/oneapi/fortran-compiler.html
  - https://flang.llvm.org/docs/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LLVM Flang
**Goal:** use the LLVM Fortran frontend.
```bash
flang -O2 -o app main.f90
flang -fopenmp -O2 ...
```
- Flang is the LLVM Fortran compiler; the executable was called `flang-new` for some releases and is `flang` in current LLVM (confirm your install).
- Supports F2018 broadly; OpenMP supported; check docs for coverage of coarrays and newer features (unconfirmed per release).
- Uses LLVM optimisations and tools (`-flto`, sanitizers).
- Module files are incompatible with gfortran and ifx.
## Gotchas
- Warning and runtime-check flags differ from gfortran; consult `flang --help`.
- Some intrinsic or runtime features may be missing; run your test suite.
## Self-check
Build your test suite with flang and compare numerical output to gfortran.
