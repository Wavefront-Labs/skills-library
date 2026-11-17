---
id: computing-software.software-engineering.fortran.runtime-checks
name: runtime-checks
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, runtime-checks, fortran-debugging]
level: intro
status: docs-checked
description: "Enable -fcheck, -finit-real and -ffpe-trap in debug builds to catch bounds errors and FP faults."
sources:
  - https://gcc.gnu.org/onlinedocs/gfortran/
  - https://sourceware.org/gdb/documentation/
  - https://valgrind.org/docs/manual/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime checks and backtraces
**Goal:** fail loudly in debug builds.
```bash
gfortran -g -O0 -fcheck=all -ffpe-trap=invalid,zero,overflow \
         -finit-real=snan -finit-integer=-99999 -Wall -o app_dbg *.f90
```
- `-fcheck=<keywords>` enables run-time checks: `all` (all of them), `array-temps`, `bits`, `bounds`, `do` (invalid modification of loop iteration variables), `mem` (memory allocation), `pointer`, `recursion`. Prefix a keyword with `no-` to disable it.
- When a serious runtime error or a deadly signal occurs, the Fortran runtime tries to print a backtrace; `-fno-backtrace` disables that.
- `-finit-real=<zero|inf|-inf|nan|snan>` initialises local reals; `snan` gives a signalling NaN, but compile-time optimisation may turn it into a quiet NaN and trapping must be enabled (for example with `-ffpe-trap`). `-finit-integer=<n>` sets local integers.
- These `-finit-*` options do not initialise pointers, allocatable arrays or variables in `EQUIVALENCE`.
- `-ffpe-trap=` enables floating-point exception traps; none are enabled by default.
## Gotchas
- Checks cost run time; keep them out of release builds.
## Self-check
Read past the end of an array with `-fcheck=bounds` and confirm the runtime reports the out-of-bounds index.

## Checked
2026-11-02. Confirmed in invoke.texi: -fcheck keywords and no- prefix, -fno-backtrace, -finit-real/-integer and their limits, -ffpe-trap default. Removed: 'slow by large factors', -finit-integer determinism remark, exact runtime message text, -fbacktrace flag (the manual now documents -fno-backtrace).
Method: documentation only; no commands were run.
