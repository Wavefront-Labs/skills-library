---
id: computing-software.software-engineering.fortran.pointer-remapping
name: pointer-remapping
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, pointer-remapping, fortran-pointers]
level: advanced
status: draft
description: "Reshape a view of contiguous data with pointer bounds remapping p(lb:ub) => target, and treat 1-D storage as 2-D."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pointer bounds remapping
**Goal:** view the same memory with a different shape.
```fortran
real, target :: buf(12)
real, pointer :: m(:, :), v(:)
m(1:3, 1:4) => buf        ! 2-D view of 1-D storage (F2008)
v(0:11) => buf            ! new lower bound
```
- F2003 allowed remapping to a rank-1 target; F2008 also allows a simply contiguous target of any rank.
- Size of the view must not exceed the target.
## Gotchas
- A rank-changing target must be rank 1 or simply contiguous; otherwise it is an error.
- Alternatively use `reshape` for a copy.
## Self-check
Write through `m(2,2)` and read back from the right index of `buf` using column-major order.
