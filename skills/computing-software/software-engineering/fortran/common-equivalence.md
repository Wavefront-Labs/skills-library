---
id: computing-software.software-engineering.fortran.common-equivalence
name: common-equivalence
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, common-equivalence, fortran-legacy]
level: practitioner
status: draft
description: "Replace common blocks and equivalence with modules and derived types while preserving behaviour."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://fortran-lang.org/learn/best_practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# common blocks and equivalence
**Goal:** modernise shared state.
- `common /grid/ nx, ny, dx` shares storage by position; names may differ between program units.
- Replace with a module:
```fortran
module grid_mod
  implicit none
  integer :: nx, ny
  real :: dx
end module
```
- Replace each `common /grid/` by `use grid_mod` in every unit that referenced it; check ordering and types matched.
- `equivalence (a, b)` overlays storage (type punning). Replace with `transfer(a, mold)` when you need reinterpretation.
- `block data` initialises common blocks; fold into module initialisation.
## Gotchas
- Different units may declare the common block with different layouts; reconcile before replacing.
- gfortran warns on mismatched common sizes only with `-Wall` and link-time info (`-flto`).
## Self-check
Run the program's regression tests before and after; outputs identical.
