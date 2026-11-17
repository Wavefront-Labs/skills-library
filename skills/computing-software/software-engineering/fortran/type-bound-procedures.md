---
id: computing-software.software-engineering.fortran.type-bound-procedures
name: type-bound-procedures
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, type-bound-procedures, fortran-oop]
level: practitioner
status: docs-checked
description: "Attach procedures to a derived type with contains and procedure, with the passed-object dummy class(t)."
sources:
  - https://fortran-lang.org/learn/quickstart/derived_types
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type-bound procedures
**Goal:** give types methods.
```fortran
type :: counter
  integer :: n = 0
contains
  procedure :: inc
end type
subroutine inc(self)
  class(counter), intent(inout) :: self
  self%n = self%n + 1
end subroutine
```
- Call as `call c%inc()`; the object is passed implicitly as the argument that `self` (a name of your choice) receives.
- Bindings follow `contains` after the components; the procedure itself is defined in the module's own `contains` section.
- A type-bound function is called inside an expression (`x = sq%area()`); a type-bound subroutine is called with `call`.
## Gotchas
- Declaring the object dummy as `class(counter)` instead of `type(counter)` lets the procedure accept any type that extends `counter`.
## Self-check
Call `inc` twice and confirm `c%n` is 2.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn quickstart page Derived types (section Type-bound procedures): `contains`, `procedure ::`, `self`, `class(t)`, function versus subroutine call forms. Removed: `nopass`, `pass(name)`, `generic`, `private` bindings and the `=>` renaming form, which no page read covers.
Method: documentation only; no commands were run.
