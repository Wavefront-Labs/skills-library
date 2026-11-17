---
id: computing-software.software-engineering.fortran.iso-fortran-env-kinds
name: iso-fortran-env-kinds
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, iso-fortran-env-kinds, fortran-kinds]
level: intro
status: draft
description: "Use int8..int64, real32, real64, real128 and character_kinds from the intrinsic module iso_fortran_env for portable numeric types."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Named kinds from iso_fortran_env
**Goal:** get portable kind names without selected_real_kind boilerplate.
- `iso_fortran_env` (F2008) provides `int8, int16, int32, int64`, `real32, real64, real128`, `logical_kinds`, `character_kinds`.
- A kind may be negative if the compiler does not support that size (e.g. `real128` on a target without quad precision).
```fortran
use, intrinsic :: iso_fortran_env, only: sp => real32, dp => real64, i8 => int64
integer, parameter :: wp = dp      ! single place to switch working precision
real(wp) :: x
```
- Also exported: `input_unit`, `output_unit`, `error_unit` for stdin, stdout, stderr.
## Gotchas
- `real128` is software quad on gfortran for most targets and is slow.
- `kind(1.0d0)` is not guaranteed to be 8; use named kinds.
## Self-check
`print *, real64, real128` prints positive kind values on gfortran; confirm no negative numbers.
