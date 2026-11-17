---
id: computing-software.software-engineering.fortran.integer-real-types
name: integer-real-types
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, integer-real-types, fortran-intrinsic-types]
level: intro
status: docs-checked
description: "Declare integer and real variables with explicit kind parameters instead of nonstandard real*8 or double precision shortcuts."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integer and real types
**Goal:** pick precise numeric types and avoid compiler-dependent widths.
- Use named kinds: `integer(int64)`, `real(real64)` from `iso_fortran_env`. The manual recommends the `SELECTED_*_KIND` intrinsics or the `INT8`..`INT64`, `REAL32`, `REAL64`, `REAL128` parameters of `ISO_FORTRAN_ENV` instead of concrete kind numbers; the arrays `INTEGER_KINDS` and `REAL_KINDS` in that module list the available kinds.
- For gfortran the KIND value matches the storage size in bytes (except `COMPLEX`), but do not depend on it.
```fortran
use, intrinsic :: iso_fortran_env, only: real64, int64
real(real64) :: x = 0.1_real64
integer(int64) :: n = 10_int64**12
```
- `huge(x)` returns the largest number that is not an infinity in the model of the type of `x`; `epsilon(x)` is the smallest `E` of the same kind with `1 + E > 1`.
## Gotchas
- Give literals the intended kind (`0.1_real64`); an unsuffixed literal has the default real kind.
## Self-check
Print `huge(1_int64)` and `epsilon(1.0_real64)` and compare with your expectation.

## Checked
2026-11-02. Confirmed in gfortran.texi (ISO_FORTRAN_ENV kinds, KIND = storage size note) and intrinsic.texi (HUGE, EPSILON). Removed: 'default integer and real are 32-bit', real*8/integer*4 extension comment, overflow-undefined claim, specific printed values (not stated on the pages read).
Method: documentation only; no commands were run.
