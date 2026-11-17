---
id: computing-software.software-engineering.fortran.allocatable-arrays
name: allocatable-arrays
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, allocatable-arrays, fortran-dynamic-arrays]
level: intro
status: docs-checked
description: "Use allocatable arrays instead of pointers; allocate, test with allocated, and rely on automatic deallocation at scope exit."
sources:
  - https://fortran-lang.org/learn/best_practices/allocatable_arrays
  - https://gcc.gnu.org/onlinedocs/gfortran/Code-Gen-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Allocatable arrays and automatic deallocation
**Goal:** manage dynamic memory safely.
```fortran
real, allocatable :: a(:, :)
allocate(a(n, m), source=0.0)
print *, allocated(a)
! no deallocate needed for locals
```
- Local allocatables are deallocated automatically when they go out of scope, so they cannot leak (unlike pointers).
- gfortran reallocates an allocatable left-hand side of an intrinsic assignment when it is unallocated or has a different shape (`-frealloc-lhs`, on by default except with `-std=f95`; `-Wrealloc-lhs` warns).
- `allocate` does not initialise; `source=` initialises from a scalar or array value.
- A dummy that is `allocatable, intent(out)` is deallocated on entry; `move_alloc` moves an allocation between arrays.
## Gotchas
- An allocated array cannot be allocated again, and only allocated arrays can be deallocated: guard with `allocated`.
- Passing an unallocated array to a non-allocatable dummy is an invalid memory access.
## Self-check
Allocate an array, test `allocated`, deallocate it, and test again.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn page Allocatable Arrays (automatic deallocation, `allocated`, `intent(out)`, re-allocation rule, `move_alloc`, `source=`) and the gfortran Code Generation Options page (`-frealloc-lhs`) and Error and Warning Options page (`-Wrealloc-lhs`). Removed: `stat=`, `mold=`, the `a(:) =` performance advice and the `-fcheck=all` double-allocation claim, which no page read covers.
Method: documentation only; no commands were run.
