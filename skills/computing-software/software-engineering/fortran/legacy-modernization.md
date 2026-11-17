---
id: computing-software.software-engineering.fortran.legacy-modernization
name: legacy-modernization
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, legacy-modernization, fortran-legacy]
level: sme
status: draft
description: "Plan an incremental move from FORTRAN 77 to modern Fortran with tests, free-form conversion, implicit none and modules."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://fortran-lang.org/learn/best_practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Modernisation workflow for legacy code
**Goal:** modernise safely.
- Step 0: build a regression suite on the old code (golden outputs, tolerance compare).
- Step 1: compile with maximal warnings, `-fcheck=all`, `-std=legacy` to baseline.
- Step 2: add `implicit none` per file, fix declarations.
- Step 3: convert to free form (tools: `findent`, `fprettify`, or `convert` helpers in the community; verify output).
- Step 4: wrap routines into modules; explicit interfaces expose argument mismatches.
- Step 5: replace `common`, `equivalence`, `goto`s; adopt `intent` and `allocatable`.
- Step 6: add unit tests (test-drive/pFUnit).
## Gotchas
- Never combine refactoring and behaviour changes in one commit.
- Floating-point reordering by array syntax can change low-order digits; compare with tolerance.
## Self-check
Every step keeps the regression suite green.
