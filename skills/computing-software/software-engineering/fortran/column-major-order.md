---
id: computing-software.software-engineering.fortran.column-major-order
name: column-major-order
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, column-major-order, fortran-arrays-basics]
level: practitioner
status: docs-checked
description: "Remember that Fortran stores arrays column-major (first subscript fastest) and order loops to match."
sources:
  - https://fortran-lang.org/learn/quickstart/arrays_strings
  - https://fortran-lang.org/learn/intrinsics/RESHAPE
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Column-major storage order
**Goal:** iterate in memory order.
- Element order for `a(2,3)`: `a(1,1), a(2,1), a(1,2), a(2,2), a(1,3), a(2,3)`.
- Innermost loop should vary the first (leftmost) index.
```fortran
do j = 1, n
  do i = 1, m
    a(i, j) = a(i, j) + b(i, j)
  end do
end do
```
- `reshape(..., order=[2, 1])` changes fill order.
## Gotchas
- `reshape` uses the natural (column-major) ordering unless `order=` is given.
## Self-check
Print `reshape([1, 2, 3, 4, 5, 6], [2, 3])` with and without `order=[2, 1]` and compare the fill order.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn page Arrays and strings (column-major, first index varies fastest) and the `reshape` intrinsic page (`order` argument, natural ordering). Removed: C row-major interop advice, the NumPy `order='F'` note and the timing claim, which no page read covers.
Method: documentation only; no commands were run.
