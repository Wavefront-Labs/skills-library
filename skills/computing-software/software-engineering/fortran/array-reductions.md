---
id: computing-software.software-engineering.fortran.array-reductions
name: array-reductions
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, array-reductions, fortran-array-ops]
level: practitioner
status: docs-checked
description: "Use sum, product, maxval, minval, maxloc, minloc, count, any, all with dim and mask arguments."
sources:
  - https://fortran-lang.org/learn/intrinsics/MAXLOC
  - https://fortran-lang.org/learn/intrinsics/MAXVAL
  - https://fortran-lang.org/learn/intrinsics/SUM
  - https://fortran-lang.org/learn/intrinsics/NORM2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reductions: sum, product, maxval, minloc and friends
**Goal:** summarise arrays with intrinsics.
```fortran
real :: a(3, 4)
print *, sum(a)               ! all elements
print *, sum(a, dim=1)        ! shape [4], column sums
print *, maxval(a, mask=a < 100.0)
print *, maxloc(a)            ! rank-1 result of size 2
print *, dot_product(a(:,1), a(:,2)), norm2(a)
```
- `norm2` is Fortran 2008 and later; the quickstart recommends it over hand-written vector norms.
- `any`/`all`/`count` take logical arrays.
- `maxloc` returns offsets from the start of the array, not subscripts, when the declared lower bound is not 1.
## Gotchas
- For a zero-size array or an all-false mask, `maxval` returns the most negative number of the type and `maxloc` returns zeros.
## Self-check
`sum(a, dim=2)` on a 3x4 array has size 3.

## Checked
2026-11-03. Confirmed against the fortran-lang.org intrinsic pages for `maxloc`, `maxval`, `sum` and `norm2`, and the Organising code structure page (`norm2` advice): `dim` and `mask` arguments, rank-one `maxloc` result, offset semantics, empty-array results, Fortran 2008 status of `norm2`. Removed: `findloc`, the single-precision rounding advice and the empty `sum` result, which no page read covers.
Method: documentation only; no commands were run.
