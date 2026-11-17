---
id: computing-software.software-engineering.fortran.ieee-arithmetic
name: ieee-arithmetic
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, ieee-arithmetic, fortran-ieee]
level: advanced
status: docs-checked
description: "Detect NaN with ieee_is_nan and understand how -ffast-math and max/min affect NaN handling in gfortran."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ieee_arithmetic module
**Goal:** handle special floating-point values.
```fortran
use, intrinsic :: ieee_arithmetic
if (ieee_is_nan(x)) print *, 'NaN'
```
- The `IEEE_ARITHMETIC` intrinsic module is supported by GNU Fortran; the manual names `ieee_is_nan` as the way to take specific action when an argument to `max` or `min` is a NaN.
- The manual says `max` and `min` do not specify behaviour when one argument is a NaN, so test with `ieee_is_nan` before calling them.
- `-ffast-math` includes `-ffinite-math-only`, which the GCC manual describes as assuming no NaNs and no Infs, so NaN tests can change under `-ffast-math`.
- By default no floating-point exception traps are enabled (`-ffpe-trap=` enables them).
## Gotchas
- Other module procedures (for example constructors of special values) are described in the Fortran standard, not on the pages checked here; consult the standard or the compiler's module for their exact names.
## Self-check
Test a NaN produced under your build flags with `ieee_is_nan` and confirm it reports true.

## Checked
2026-11-02. Confirmed in gfortran.texi (IEEE_ARITHMETIC support and IEEE_IS_NAN for MAX/MIN NaN handling), invoke.texi (no traps by default) and the GCC manual (-ffast-math contents). Removed: the ieee_value / ieee_class / ieee_next_after list and division-by-zero statement, which are standard-text claims not on the pages read.
Method: documentation only; no commands were run.
