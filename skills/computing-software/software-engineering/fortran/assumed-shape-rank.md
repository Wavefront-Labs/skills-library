---
id: computing-software.software-engineering.fortran.assumed-shape-rank
name: assumed-shape-rank
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, assumed-shape-rank, fortran-dynamic-arrays]
level: advanced
status: docs-checked
description: "Pass arrays with assumed-shape (:), avoid assumed-size (*), and use assumed-rank (..) with select rank."
sources:
  - https://fortran-lang.org/learn/best_practices/arrays
  - https://fortran-lang.org/learn/quickstart/organising_code
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assumed-shape, assumed-size and assumed-rank dummies
**Goal:** choose the right array dummy form.
- Assumed shape: `real, intent(in) :: x(:)` is the preferred form; shape and size are passed along and checked at compile time and optionally at run time, and strided sections are passed without a copy. A module provides the explicit interface it needs.
- Assumed size: `x(*)` gives the least checking, is common in legacy code, and cannot be used with many intrinsics such as `size` and `shape`; avoid it.
- Explicit shape: `x(n)` requires the extent as another argument, the shape is not checked, and it needs contiguous memory (a temporary is made for strided actuals).
- Assumed rank (F2018): `real :: x(..)` with `select rank`:
```fortran
select rank (x)
rank (1); print *, size(x)
rank (2); print *, shape(x)
end select
```
- For a lower bound other than 1, declare it: `real(dp), intent(in) :: lam(kappa_min:)`.
## Gotchas
- Explicit-shape dummies do not check the shape, so a wrong extent silently reinterprets the same memory.
## Self-check
Pass a strided section such as `r(1:10:2)` to an assumed-shape dummy and confirm `size` reports 5.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn pages Arrays (assumed-shape, assumed-rank with `select rank` introduced in Fortran 2018, explicit-shape, assumed-size, lower bound syntax) and Organising code structure (modules supply the explicit interface). Removed: the `contiguous` claim, the lower-bound-resets claim, the no-interface crash claim and the `rank default` branch, which no page read covers.
Method: documentation only; no commands were run.
