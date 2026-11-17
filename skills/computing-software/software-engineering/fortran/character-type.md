---
id: computing-software.software-engineering.fortran.character-type
name: character-type
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, character-type, fortran-intrinsic-types]
level: intro
status: docs-checked
description: "Declare fixed-length character variables, understand blank padding and trim, and use the len=* assumed length form."
sources:
  - https://fortran-lang.org/learn/quickstart/arrays_strings
  - https://fortran-lang.org/learn/intrinsics/TRIM
  - https://fortran-lang.org/learn/intrinsics/LEN_TRIM
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Character type and length
**Goal:** use fixed and assumed-length characters correctly.
- `character(len=20) :: name` is fixed length; values in a `character` array are truncated or right-padded with blanks to the declared length.
- Dummy arguments use `character(len=*)` to inherit the actual length.
- Use `trim(s)` to drop trailing blanks, `len_trim(s)` for the length without them.
```fortran
character(len=8) :: a = 'hello'     ! stored 'hello   '
print *, len(a), len_trim(a)        ! 8 5
subroutine show(s)
  character(len=*), intent(in) :: s
  print *, trim(s)
end subroutine
```
- `character(len=:), allocatable` gives deferred length (see the deferred-length skill).
## Gotchas
- `trim` removes trailing blank characters; `len_trim` returns the length ignoring them.
## Self-check
Confirm the example above prints 8 and 5.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn page Arrays and strings (fixed `len`, `len=*` dummy, padding and truncation in character arrays) and the intrinsic pages for `trim` and `len_trim`. Removed: the `kind` mention, the comparison rule and the silent-truncation claim for scalar assignment, which no page read covers.
Method: documentation only; no commands were run.
