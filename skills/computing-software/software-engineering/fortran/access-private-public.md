---
id: computing-software.software-engineering.fortran.access-private-public
name: access-private-public
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, access-private-public, fortran-modules]
level: practitioner
status: draft
description: "Hide module internals with private by default, export a minimal public API, and use protected for read-only module variables."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://fortran-lang.org/learn/best_practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# private, public and protected
**Goal:** define clean module APIs.
```fortran
module stack_mod
  implicit none
  private                     ! default private
  public :: stack, push
  integer, public, protected :: count = 0
  type :: stack
    private
    integer, allocatable :: items(:)
  end type
end module
```
- `protected` variables are readable outside but modifiable only inside the module.
- Per-type `private` hides components, whole-type `private` statement hides the type name.
## Gotchas
- A public procedure cannot use a private type in its interface without the compiler warning/error (accessibility rules).
- `protected` applies only to module variables, not to components.
## Self-check
Try to assign the protected variable outside the module; it must fail to compile.
