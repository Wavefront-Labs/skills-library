---
id: computing-software.software-engineering.fortran.whole-array-expressions
name: whole-array-expressions
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, whole-array-expressions, fortran-array-ops]
level: intro
status: docs-checked
description: "Write array arithmetic without loops, apply elemental intrinsics to arrays, and use conformable operands."
sources:
  - https://fortran-lang.org/learn/quickstart/arrays_strings
  - https://fortran-lang.org/learn/best_practices/element_operations
  - https://gcc.gnu.org/onlinedocs/gfortran/Error-and-Warning-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Whole-array expressions and elemental application
**Goal:** replace loops with array expressions.
```fortran
real :: a(100), b(100), c(100)
c = a * b + 2.0           ! elementwise
c = sqrt(abs(a))          ! elemental intrinsic
a(2:99) = 0.5 * (b(1:98) + b(3:100))   ! stencil
```
- Operands must be arrays of the same shape, or scalars; other combinations are a compiler error.
- User-defined `elemental` procedures work the same way.
- Array constructors build values: `[1, 2, 3]` and `[(i, i = 1, 10)]`.
## Gotchas
- The compiler may create array temporaries; gfortran's `-Warray-temporaries` reports them.
## Self-check
Compare the stencil line with an explicit `do` loop on a small array and confirm equal results.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn pages Arrays and strings (slicing, constructors) and Element-wise Operations on Arrays (same-shape-or-scalar rule), the intrinsic pages for `sqrt` and `abs` (elemental), and the gfortran Error and Warning Options page (`-Warray-temporaries`). Removed: the overlapping-assignment evaluation claim and the zero-sized array claim, which no page read covers.
Method: documentation only; no commands were run.
