---
id: computing-software.software-engineering.fortran.pure-elemental
name: pure-elemental
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, pure-elemental, fortran-procedures]
level: practitioner
status: docs-checked
description: "Mark side-effect-free procedures pure and scalar procedures elemental so they apply to arrays of any shape."
sources:
  - https://fortran-lang.org/learn/best_practices/element_operations
  - https://fortran-lang.org/learn/quickstart/organising_code
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pure and elemental procedures
**Goal:** write procedures that parallelise and vectorise.
```fortran
elemental function clamp(x, lo, hi) result(r)
  real, intent(in) :: x, lo, hi
  real :: r
  r = min(max(x, lo), hi)
end function
y = clamp(x, 0.0, 1.0)     ! x is an array
```
- `pure` function: all arguments `intent(in)`, no side effects.
- `elemental` implies `pure`: it can only use `pure` procedures and has no side effects.
- All arguments of an elemental procedure must be scalars; if one actual argument is an array, the others must be arrays of the same shape or scalars.
## Gotchas
- Arguments that cannot be combined by that rule give a compiler error.
## Self-check
Call `clamp` with an array and scalar bounds and confirm the result has the shape of the array.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn pages Element-wise Operations on Arrays (elemental implies pure, scalar arguments, shape rule, compiler error) and Organising code structure (pure functions). Removed: pure restrictions on I/O, `stop`, `impure elemental`, the `error stop` note and the `do concurrent` claim, which no page read covers.
Method: documentation only; no commands were run.
