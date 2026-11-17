---
id: computing-software.software-engineering.fortran.structure-constructors
name: structure-constructors
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, structure-constructors, fortran-derived-types]
level: practitioner
status: draft
description: "Build derived-type values with structure constructors, using keyword components and defaults, and wrap them in constructor functions."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Structure constructors
**Goal:** construct values safely.
- A structure constructor has the type name: `p = point(1.0, 2.0)` or `point(y=2.0)` with keywords; omitted components need defaults.
- A generic interface with the same name as the type creates a user constructor.
```fortran
interface point
  module procedure make_point
end interface
...
function make_point(r, theta) result(p)
  real, intent(in) :: r, theta
  type(point) :: p
  p = point(r*cos(theta), r*sin(theta))
end function
```
## Gotchas
- With private components, the structure constructor is usable outside the module only in F2008+ when components are accessible; use a user-defined constructor to be safe.
- Positional constructor calls break when components are reordered; prefer keywords.
## Self-check
Call `point(y=3.0)` and verify `x` is 0.0.
