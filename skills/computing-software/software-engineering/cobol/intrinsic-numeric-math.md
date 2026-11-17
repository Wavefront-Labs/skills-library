---
id: computing-software.software-engineering.cobol.intrinsic-numeric-math
name: intrinsic-numeric-math
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, intrinsic-numeric-math, cobol-intrinsic, function-mod, function-max, function-sqrt, function-rem]
level: practitioner
status: docs-checked
description: "Use FUNCTION MOD, REM, MAX, MIN, SQRT, INTEGER, ABS, SUM and friends instead of hand-rolled arithmetic."
sources:
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric and mathematical intrinsic functions
**Goal:** reach for standard functions.
```cobol
COMPUTE WS-R   = FUNCTION MOD(WS-N, 7)
COMPUTE WS-HI  = FUNCTION MAX(WS-A, WS-B, WS-C)
COMPUTE WS-SQ  = FUNCTION SQRT(WS-X)
COMPUTE WS-AVG = FUNCTION MEAN(A, B, C)
COMPUTE WS-I   = FUNCTION INTEGER(WS-X)         *> floor
```
- `INTEGER(number)` returns the greatest integer less than or equal to the number (floor).
- `MOD(value, modulus)` and `REM(number, divisor)` return remainders; arguments can be non-integer.
- Also in the Guide: INTEGER-PART, FACTORIAL, ANNUITY, PRESENT-VALUE, MIDRANGE, MEDIAN, RANGE, VARIANCE, STANDARD-DEVIATION, LOG, LOG10, EXP, PI, E, SQRT, MAX, MEAN.
- `cobc --list-intrinsics` lists the functions of your build.

## Gotchas
- Check the sign of results for negative operands with a small test on your own build before relying on MOD or REM.

## Self-check
Print `FUNCTION MOD(-7, 3)` and `FUNCTION REM(-7, 3)` on your build.

## Checked
2026-11-02. Checked against the GnuCOBOL Programmer's Guide function entries INTEGER, MOD, REM and the function list. Removed: the sign semantics of MOD and REM (not stated), the expected values 2 and -1, the SIN/COS/TAN family claim, the table-argument `ALL` example, the IBM REPOSITORY shortcut, and the floating-point precision remark.

Method: documentation only; no commands were run.
