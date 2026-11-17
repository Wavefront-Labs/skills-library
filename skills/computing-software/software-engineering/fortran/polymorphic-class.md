---
id: computing-software.software-engineering.fortran.polymorphic-class
name: polymorphic-class
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, polymorphic-class, fortran-oop]
level: advanced
status: docs-checked
description: "Use class(t) dummies so one procedure accepts a type and its extensions, and compare dynamic types."
sources:
  - https://fortran-lang.org/learn/quickstart/derived_types
  - https://fortran-lang.org/learn/intrinsics/SAME_TYPE_AS
  - https://fortran-lang.org/learn/intrinsics/EXTENDS_TYPE_OF
  - https://fortran-lang.org/learn/best_practices/allocatable_arrays
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Polymorphic class entities
**Goal:** write code that handles any extension of a type.
- A `class(shape)` dummy accepts `shape` or any type that extends it; the keyword `class` introduces polymorphism.
- `allocate(x, source=y)` allocates from a scalar or array source.
- `same_type_as(a, b)` and `extends_type_of(a, b)` compare dynamic types (Fortran 2003 and later); neither argument may have an undefined association status.
```fortran
subroutine describe(s)
  class(shape), intent(in) :: s
  print *, same_type_as(s, s)
end subroutine
```
## Gotchas
- Declaring the dummy as `type(shape)` instead of `class(shape)` rejects extensions of `shape`.
## Self-check
Pass a `circle` to `describe` and confirm it is accepted.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn page Derived types (`class(t)` accepts extensions) and the intrinsic pages for `same_type_as` and `extends_type_of`, and the Allocatable Arrays page (`source=`). Removed: `class(*)`, `select type`, `mold=`, heterogeneous-array and compiler-bug notes, and the polymorphic allocatable example, which no page read covers.
Method: documentation only; no commands were run.
