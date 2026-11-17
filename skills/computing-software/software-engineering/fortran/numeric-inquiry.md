---
id: computing-software.software-engineering.fortran.numeric-inquiry
name: numeric-inquiry
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, numeric-inquiry, fortran-numeric-intrinsics]
level: practitioner
status: docs-checked
description: "Query type limits with huge, tiny, epsilon, digits, precision, range, spacing and nearest."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric inquiry functions
**Goal:** write kind-independent numeric code.
```fortran
use, intrinsic :: iso_fortran_env, only: dp => real64
real(dp) :: x
print *, epsilon(x), tiny(x), huge(x), digits(x), precision(x), range(x)
print *, spacing(1.0_dp), nearest(1.0_dp, 1.0_dp) - 1.0_dp
```
- `epsilon(x)` is the smallest `E` of the same kind as `x` such that `1 + E > 1`; `tiny(x)` the smallest positive (non-zero) number in the model of the type; `huge(x)` the largest number that is not an infinity in the model.
- `digits(x)` returns the number of significant binary digits of the model (the manual gives 24 as the likely value for a default 32-bit real); `precision(x)` the decimal precision and `range(x)` the decimal exponent range.
- `spacing(x)` is the distance between `x` and the nearest adjacent number of the same type; `nearest(x, s)` returns the nearest representable number in the direction of the sign of `s` (`s` must not be zero).
- `bit_size(i)` gives the number of bits of an integer type.
## Gotchas
- `epsilon` relates to the spacing at 1; use `spacing(x)` for the local resolution at `x`.
## Self-check
Print `epsilon(1.0)` and `epsilon(1.0d0)` and compare them.

## Checked
2026-11-02. Confirmed in intrinsic.texi: EPSILON, TINY, HUGE, DIGITS, PRECISION, RANGE, SPACING, NEAREST, BIT_SIZE. Removed: huge-overflow guard example, -huge(int)-1 note, real64-vs-dp alias claim (iso_fortran_env real64 exists per gfortran.texi).
Method: documentation only; no commands were run.
