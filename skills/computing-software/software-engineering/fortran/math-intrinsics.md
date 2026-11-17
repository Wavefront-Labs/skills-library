---
id: computing-software.software-engineering.fortran.math-intrinsics
name: math-intrinsics
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, math-intrinsics, fortran-numeric-intrinsics]
level: intro
status: draft
description: "Use sqrt, exp, log, trig and hyperbolic functions, mod versus modulo, and F2008 additions such as hypot, gamma, bessel."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mathematical intrinsics
**Goal:** pick the right math function.
- Standard: `sqrt exp log log10 sin cos tan asin acos atan atan2 sinh cosh tanh`.
- F2008: `hypot(x, y)`, `gamma`, `log_gamma`, `erf`, `erfc`, `bessel_j0`, `norm2`, `acosh/asinh/atanh`.
- `mod(a, p)` has the sign of `a`; `modulo(a, p)` has the sign of `p`.
- `floor`, `ceiling`, `nint`, `int` (truncate toward zero); `aint`, `anint` return reals.
```fortran
print *, mod(-7, 3), modulo(-7, 3)     ! -1  2
print *, nint(2.5), nint(-2.5)         ! 3 -3
```
- `sign(a, b)` gives |a| with the sign of b; `epsilon(x)` is machine epsilon.
## Gotchas
- Integer division truncates: `7/2` is 3.
- `x**2` is optimised; `x**2.0` may call pow.
## Self-check
Evaluate the printed example and confirm the comments.
