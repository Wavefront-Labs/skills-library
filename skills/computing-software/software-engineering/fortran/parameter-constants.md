---
id: computing-software.software-engineering.fortran.parameter-constants
name: parameter-constants
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, parameter-constants, fortran-declarations]
level: intro
status: draft
description: "Declare compile-time constants with the parameter attribute and use them for array sizes and kinds."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://fortran-lang.org/learn/best_practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Named constants with parameter
**Goal:** define constants once.
- `real, parameter :: pi = 3.14159265358979323846_dp`; value must be a constant expression.
- Array constants may use implied shape: `integer, parameter :: primes(*) = [2, 3, 5, 7]`.
- Character: `character(len=*), parameter :: version = '1.2.3'` takes its length from the value.
```fortran
integer, parameter :: n = 100
real(dp) :: grid(n)
```
## Gotchas
- A `parameter` cannot be modified or passed to `intent(out)` or `intent(inout)`.
- `parameter` initialisation of reals needs the kind suffix or precision is lost.
## Self-check
Try to assign to a parameter and verify the compiler rejects it.
