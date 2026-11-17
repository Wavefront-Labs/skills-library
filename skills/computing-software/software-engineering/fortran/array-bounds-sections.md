---
id: computing-software.software-engineering.fortran.array-bounds-sections
name: array-bounds-sections
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, array-bounds-sections, fortran-arrays-basics]
level: intro
status: docs-checked
description: "Declare arrays with explicit bounds, take sections with triplets, and use size, shape, lbound and ubound."
sources:
  - https://fortran-lang.org/learn/quickstart/arrays_strings
  - https://fortran-lang.org/learn/best_practices/arrays
  - https://gcc.gnu.org/onlinedocs/gfortran/Code-Gen-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Array bounds, shape and sections
**Goal:** slice and query arrays safely.
```fortran
real :: a(0:9), b(3, 4)
print *, size(b), shape(b), lbound(a), ubound(a)   ! 12  3 4  0  9
a(2:8:2) = 1.0        ! start:stop:stride
b(:, 2) = 0.0         ! second column
```
- Arrays are one-based by default; `a(0:9)` and `a(-5:5)` set custom bounds.
- Strided sections such as `r(1:10:2)` pass to assumed-shape dummies without a copy; explicit-shape dummies need contiguous memory and get a temporary.
- Arrays are stored in column-major order: the first index varies fastest.
## Gotchas
- gfortran's `-fcheck=bounds` adds run-time checks of array subscripts against the declared bounds.
## Self-check
Compile with `-fcheck=bounds` and confirm `a(10)` is reported at run time.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn pages Arrays and strings (declaration, bounds, slicing with stride, column-major) and Arrays (strided sections, explicit-shape temporaries), plus the gfortran Code Generation Options page (`-fcheck=bounds`). Removed: the rank-15 limit, the non-contiguous `a(::2)` note and the undefined-behaviour claim, which no page read covers.
Method: documentation only; no commands were run.
