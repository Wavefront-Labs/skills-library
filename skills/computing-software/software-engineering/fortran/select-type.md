---
id: computing-software.software-engineering.fortran.select-type
name: select-type
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, select-type, fortran-control-flow]
level: advanced
status: draft
description: "Recover the dynamic type of a class(*) or class(t) entity with select type, type is, class is and class default."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# select type construct
**Goal:** dispatch on dynamic type.
```fortran
subroutine show(x)
  class(*), intent(in) :: x
  select type (x)
  type is (integer);  print *, 'int', x
  type is (real);     print *, 'real', x
  class is (shape);   print *, 'shape area', x%area()
  class default;      print *, 'unknown'
  end select
end subroutine
```
- `type is` matches exactly; `class is` matches the type or an extension; the most specific match wins.
- Associate-name: `select type (s => obj%field)`.
- `type is (character(len=*))` matches any length.
## Gotchas
- Order of `class is` blocks does not matter; the matching rule is by specificity.
- `type is` for intrinsic types needs the kind to match, so `real(8)` will not match `type is (real)`.
## Self-check
Pass an `integer(8)`; confirm it hits `class default` unless you add a matching clause.
