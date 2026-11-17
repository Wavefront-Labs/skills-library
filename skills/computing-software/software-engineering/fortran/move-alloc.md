---
id: computing-software.software-engineering.fortran.move-alloc
name: move-alloc
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, move-alloc, fortran-dynamic-arrays]
level: advanced
status: docs-checked
description: "Grow arrays cheaply with move_alloc, which transfers an allocation without copying."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://fortran-lang.org/learn/best_practices/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# move_alloc and resizing
**Goal:** resize allocatables with minimal copying.
```fortran
subroutine grow(a, newn)
  integer, allocatable, intent(inout) :: a(:)
  integer, intent(in) :: newn
  integer, allocatable :: tmp(:)
  allocate(tmp(newn))
  tmp(1:size(a)) = a
  tmp(size(a)+1:) = 0
  call move_alloc(from=tmp, to=a)
end subroutine
```
- `move_alloc(from, to)` moves the allocation from `from` to `to`; `from` becomes deallocated. `from` is `allocatable, intent(inout)` of any type and kind; `to` is `allocatable, intent(out)` of the same type, kind and rank.
- It is a Fortran 2003 intrinsic subroutine.
## Gotchas
- `a` must be allocated before `size(a)` is read in the example.
- Assigning `tmp(1:size(a)) = a` still copies the old data.
## Self-check
Call `grow` and check `allocated(tmp)` is false after `move_alloc`.

## Checked
2026-11-02. Confirmed in intrinsic.texi: MOVE_ALLOC semantics, argument attributes, standard. Removed: polymorphic/coarray/scalar support list, amortised O(1) growth claim (not stated).
Method: documentation only; no commands were run.
