---
id: computing-software.software-engineering.fortran.module-basics
name: module-basics
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, module-basics, fortran-modules]
level: intro
status: docs-checked
description: "Organise code in modules with specification part and contains section, one module per file named after the module."
sources:
  - https://fortran-lang.org/learn/quickstart/organising_code
  - https://fortran-lang.org/learn/best_practices/modules_programs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module structure
**Goal:** structure projects in modules.
```fortran
module geometry
  use, intrinsic :: iso_fortran_env, only: dp => real64
  implicit none
  private
  public :: area
  real(dp), parameter :: pi = acos(-1.0_dp)
contains
  pure function area(r) result(a)
    real(dp), intent(in) :: r
    real(dp) :: a
    a = pi * r**2
  end function
end module geometry
```
- Order: `use`, `implicit none`, `private`/`public`, declarations, `contains`, procedures.
- Use a module with `use geometry`, or import selected names with `use geometry, only: area` (`only: alias => area` renames).
- Module procedures get explicit interfaces automatically.
- Keep one module per source file, with the module name matching the file path; prefix module names with the library name to avoid clashes.
- Module variables are implicitly saved; limit them to parameters, or export them `protected` rather than `public`.
## Gotchas
- Modules need to be compiled before any program unit that uses them.
## Self-check
Write a small program that uses `geometry` with `only: area` and confirm it builds after the module.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn pages Organising code structure and Modules and Programs: module layout, `private`/`public`, `use ... only` and renaming, one module per file, saved module variables, compile order. The `iso_fortran_env` `real64` import matches the Variables page. Removed: `.mod` file claims and the compiler-specific `.mod` note, which no page read covers.
Method: documentation only; no commands were run.
