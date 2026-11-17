---
id: computing-software.software-engineering.fortran.standard-versions
name: standard-versions
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, standard-versions, fortran-standards]
level: intro
status: draft
description: "Know the Fortran standard history 77, 90, 95, 2003, 2008, 2018, 2023 and what each added, and select with std flags."
sources:
  - https://j3-fortran.org/
  - https://wg5-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fortran standard versions
**Goal:** target the right standard.
- F77: fixed form, structured control. F90: free form, modules, array syntax, allocatable, pointers. F95: forall, pure/elemental. F2003: OOP, C interop, IEEE, allocatable components, stream I/O. F2008: coarrays, submodules, do concurrent, `block`, `contiguous`, `newunit`. F2018: collectives, teams, events, `implicit none (external)`, assumed rank. F2023: see the F2023 skill.
- gfortran: `-std=f95|f2003|f2008|f2018|f2023|gnu|legacy` (f2023 in recent versions; check your release).
- Standard text and drafts are on j3-fortran.org; WG5 on wg5-fortran.org.
## Gotchas
- The default `-std=gnu` accepts extensions; use `-std=f2018` in CI to find non-portable code.
- Compiler support for newer features lags; check release notes.
## Self-check
Compile a file with `-std=f95` to see which post-95 features it uses.
