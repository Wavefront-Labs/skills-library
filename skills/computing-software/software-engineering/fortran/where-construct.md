---
id: computing-software.software-engineering.fortran.where-construct
name: where-construct
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, where-construct, fortran-array-ops]
level: practitioner
status: draft
description: "Apply conditional array assignment with where, elsewhere and masked intrinsics instead of if inside loops."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# where and elsewhere masking
**Goal:** mask array updates.
```fortran
where (x > 0.0)
  y = sqrt(x)
elsewhere (x < 0.0)
  y = -sqrt(-x)
elsewhere
  y = 0.0
end where
```
- Single-statement form: `where (x /= 0.0) y = 1.0 / x`.
- Masks must be conformable with all assigned arrays.
- Functions called inside `where` must be elemental.
- Intrinsics with `mask=`: `sum(x, mask=x > 0)`, `maxval`, `count`, `merge(a, b, mask)`.
## Gotchas
- Only masked elements are assigned, but the compiler may still evaluate the right-hand side for all elements; do not rely on the mask to avoid a floating-point exception (e.g. `1/x` with `x == 0`) when traps are enabled.
- `where` cannot contain nested non-`where` statements such as `if`.
## Self-check
Run with a negative, zero, and positive element and verify each branch.
