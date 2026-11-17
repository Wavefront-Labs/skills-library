---
id: computing-software.software-engineering.fortran.procedure-pointers
name: procedure-pointers
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, procedure-pointers, fortran-interfaces]
level: advanced
status: draft
description: "Pass procedures as arguments and store them in procedure pointers using abstract interfaces for callbacks."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Procedure pointers and callbacks
**Goal:** implement callbacks and strategies.
```fortran
abstract interface
  function f_i(x) result(y)
    real, intent(in) :: x
    real :: y
  end function
end interface
procedure(f_i), pointer :: f => null()
f => my_square
print *, f(3.0)
```
- Dummy procedure argument: `procedure(f_i) :: f`.
- Derived types can hold `procedure(f_i), pointer, nopass :: f` components.
- `associated(f)` tests a procedure pointer.
## Gotchas
- Target procedure must have a matching characteristics (same interface); internal procedures may be passed but not stored beyond host lifetime.
- Calling a null procedure pointer crashes.
## Self-check
Integrate two different functions through the same callback argument.
