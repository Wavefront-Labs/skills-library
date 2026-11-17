---
id: computing-software.software-engineering.fortran.abstract-deferred
name: abstract-deferred
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, abstract-deferred, fortran-oop]
level: advanced
status: draft
description: "Declare abstract types with deferred type-bound procedures to define interfaces that extensions must implement."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Abstract types and deferred procedures
**Goal:** define a contract for implementers.
```fortran
type, abstract :: shape
contains
  procedure(area_i), deferred :: area
end type
abstract interface
  function area_i(self) result(a)
    import :: shape
    class(shape), intent(in) :: self
    real :: a
  end function
end interface
```
- You cannot declare `type(shape)` of an abstract type, only `class(shape)`.
- A non-abstract extension must implement every deferred binding.
- `import` is needed inside interface bodies to see the host type.
## Gotchas
- Forgetting `import :: shape` produces an unknown-type error in the interface body.
- Abstract types may still hold components and non-deferred methods.
## Self-check
Extend `shape` without implementing `area` and verify the compiler rejects instantiating it.
