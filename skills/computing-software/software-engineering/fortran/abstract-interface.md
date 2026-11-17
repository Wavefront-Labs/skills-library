---
id: computing-software.software-engineering.fortran.abstract-interface
name: abstract-interface
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, abstract-interface, fortran-interfaces]
level: advanced
status: draft
description: "Declare reusable procedure signatures with abstract interface and use them for dummy procedures, pointers and deferred bindings."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Abstract interfaces
**Goal:** name a procedure signature once.
```fortran
abstract interface
  subroutine callback(i, x)
    integer, intent(in) :: i
    real, intent(in) :: x
  end subroutine
end interface
subroutine run(cb)
  procedure(callback) :: cb
end subroutine
```
- Abstract interface bodies declare no procedure; they only describe characteristics.
- `procedure(callback)` can name any procedure with that signature; `procedure(real)` style is also legal for function interface by type.
## Gotchas
- An abstract interface cannot be called.
- Include `import` for module types used in the signature.
## Self-check
Pass two different subroutines to `run` and verify each is called.
