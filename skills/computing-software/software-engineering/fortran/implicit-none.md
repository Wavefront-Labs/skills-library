---
id: computing-software.software-engineering.fortran.implicit-none
name: implicit-none
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, implicit-none, fortran-declarations]
level: intro
status: docs-checked
description: "Put implicit none in each module and program so undeclared names are compile errors."
sources:
  - https://fortran-lang.org/learn/best_practices/modules_programs
  - https://fortran-lang.org/learn/quickstart/organising_code
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# implicit none
**Goal:** eliminate typo-created variables.
- Put `implicit none` after `use` statements in each module and program.
- In a module, a single `implicit none` covers the whole module; do not repeat it in each procedure.
```fortran
module m
  implicit none
  private
contains
  ! ...
end module
```
## Self-check
Misspell a variable on purpose and confirm the compiler reports an error.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn pages Modules and Programs (`implicit none` placement and module scope) and Organising code structure (`implicit none` in modules and programs). Removed: the implicit typing rule, the `implicit none (type, external)` form, host-inheritance rules and the gfortran `-std=f2018` note, which no page read covers.
Method: documentation only; no commands were run.
