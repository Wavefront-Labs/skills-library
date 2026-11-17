---
id: computing-software.software-engineering.fortran.preprocessing-include
name: preprocessing-include
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, preprocessing-include, fortran-source-form]
level: practitioner
status: docs-checked
description: "Use the INCLUDE line and the C preprocessor (uppercase .F90 suffix or -cpp) for conditional compilation in Fortran."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# INCLUDE lines and preprocessing
**Goal:** share declarations and switch code per platform.
- `-I<dir>` affects the interpretation of the `INCLUDE` directive as well as the preprocessor's `#include`; its behaviour is similar to `-I` with `#include` in `cpp`.
- gfortran preprocesses automatically for the extensions `.fpp`, `.FPP`, `.F`, `.FOR`, `.FTN`, `.F90`, `.F95`, `.F03` and `.F08`; `-cpp` forces preprocessing of any Fortran file and `-nocpp` disables it for those extensions.
- The preprocessor runs in traditional mode, and the file-format restrictions (such as line length limits) apply to the preprocessed output too, so `-ffree-line-length-none` or `-ffixed-line-length-none` may help with long macro expansions.
```fortran
#ifdef USE_MPI
  use mpi_f08
#endif
```
Build: `gfortran -cpp -DUSE_MPI -c prog.f90`.
## Self-check
Compile with and without `-DUSE_MPI` and confirm only the intended branch is used.

## Checked
2026-11-02. Confirmed in invoke.texi: -I and INCLUDE, automatic preprocessing extension list, -cpp/-nocpp, traditional mode and line-length note. Removed: modules-preferred advice, '//' mangling claim, fpm [preprocess] table, -cpp -E self-check, mpi_f08 module name kept only as an example identifier.
Method: documentation only; no commands were run.
