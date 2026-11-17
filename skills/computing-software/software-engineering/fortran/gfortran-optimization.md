---
id: computing-software.software-engineering.fortran.gfortran-optimization
name: gfortran-optimization
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, gfortran-optimization, fortran-gfortran]
level: practitioner
status: docs-checked
description: "Choose -O levels, -ffast-math and -Ofast consequences, -flto and optimisation reports for release builds."
sources:
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optimisation and architecture flags
**Goal:** tune release builds safely.
```bash
gfortran -O2 -g -o app *.f90
gfortran -O3 -funroll-loops -o app *.f90
gfortran -O2 -ffast-math ...                    # relaxes IEEE rules
gfortran -Ofast ...                             # see below
gfortran -O2 -flto ...                          # link-time optimisation
```
- `-O0`, `-O1`, `-O2`, `-O3`, `-Os`, `-Ofast`, `-Og` are the GCC optimisation levels; `-Og` is meant for a good debugging experience.
- `-Ofast` enables all `-O3` optimisations plus `-ffast-math`, `-fallow-store-data-races`, the Fortran-specific `-fstack-arrays` (unless `-fmax-stack-var-size` is given) and `-fno-protect-parens`.
- `-ffast-math` sets `-fno-math-errno`, `-funsafe-math-optimizations`, `-ffinite-math-only`, `-fno-rounding-math`, `-fno-signaling-nans`, `-fcx-limited-range` and `-fexcess-precision=fast`; it can give incorrect output for programs that depend on exact IEEE or ISO rules.
- `-fopt-info-vec` reports vectorised loops; `-fopt-info-vec-missed` reports missed ones (for example `gcc -O2 -ftree-vectorize -fopt-info-vec-missed` in the GCC manual).
- `-march=<cpu-type>` selects the target CPU; check your target's machine options in the GCC manual for the accepted values.
## Gotchas
- `-ffinite-math-only` (part of `-ffast-math`) assumes no NaN or Inf, so NaN tests and convergence tests can change behaviour.
## Self-check
Compare timings and results at `-O0`, `-O2`, `-O3`; results should agree to tolerance.

## Checked
2026-11-02. Confirmed in the GCC manual (invoke): -O level list, -Og purpose, exact contents of -Ofast and -ffast-math, -fopt-info-vec-missed example, -march=<cpu-type> option exists. Removed: -march=native crash claim and 'safe default' wording, 'more vectorisation' for -O3, Kahan/ieee_is_nan claims, results-agree self-check kept as advice.
Method: documentation only; no commands were run.
