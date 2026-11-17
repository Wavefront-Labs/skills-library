---
id: computing-software.software-engineering.fortran.array-reshaping-packing
name: array-reshaping-packing
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, array-reshaping-packing, fortran-array-ops]
level: practitioner
status: docs-checked
description: "Restructure arrays with reshape, pack/unpack, spread, transpose, merge, cshift and eoshift."
sources:
  - https://fortran-lang.org/learn/intrinsics/RESHAPE
  - https://fortran-lang.org/learn/intrinsics/PACK
  - https://fortran-lang.org/learn/intrinsics/UNPACK
  - https://fortran-lang.org/learn/intrinsics/CSHIFT
  - https://fortran-lang.org/learn/intrinsics/SPREAD
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# reshape, pack, spread, transpose, cshift
**Goal:** rearrange arrays without loops.
```fortran
integer :: m(2, 3) = reshape([1, 2, 3, 4, 5, 6], [2, 3])
integer :: t(3, 2)
t = transpose(m)
print *, pack(m, m > 2)                 ! 1-D list of selected elements
print *, spread([1, 2, 3], dim=1, ncopies=2)
print *, cshift([1, 2, 3, 4], shift=1)  ! 2 3 4 1
```
- `unpack(vector, mask, field)` inverts `pack`.
- `merge(tsource, fsource, mask)` is an elemental conditional.
- `matmul(a, b)` multiplies matrices or matrix-vector (see BLAS skill for large sizes).
## Gotchas
- `reshape` fills in column-major order; use `order=` to change.
- With a `vector` argument, `pack` returns an array of the size of `vector`, with the selected elements first.
## Self-check
`reshape` then `transpose` a 2x3 array and verify `t(3,2)` equals `m(2,3)`.

## Checked
2026-11-03. Confirmed against the fortran-lang.org intrinsic pages for `reshape`, `pack`, `unpack`, `cshift`, `spread`, `merge`, `transpose` and `matmul`, including the `cshift` example (a shift of 1 moves elements left and wraps). Removed: the claim that `pack` follows array element order rather than row order, which no page read states.
Method: documentation only; no commands were run.
