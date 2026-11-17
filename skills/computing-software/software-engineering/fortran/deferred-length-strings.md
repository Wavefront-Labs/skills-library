---
id: computing-software.software-engineering.fortran.deferred-length-strings
name: deferred-length-strings
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, deferred-length-strings, fortran-strings]
level: practitioner
status: docs-checked
description: "Use character(len=:), allocatable for variable-length strings that resize on assignment."
sources:
  - https://fortran-lang.org/learn/quickstart/arrays_strings
  - https://gcc.gnu.org/onlinedocs/gfortran/Code-Gen-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deferred-length allocatable strings
**Goal:** get dynamic strings.
```fortran
character(len=:), allocatable :: s
s = 'abc'
s = s // 'def'          ! reallocates to length 6
print *, len(s)         ! 6
```
- Assigning to an unallocated deferred-length string allocates it with the length of the value (`last_name = 'Smith'`); `allocate(character(4) :: first_name)` sets the length explicitly.
- Elements of a `character` array share one length; strings of other lengths are truncated or right-padded.
- A `character(len=*)` dummy takes the length of the actual argument.
## Gotchas
- gfortran's `-frealloc-lhs` (default except with `-std=f95`) reallocates an allocatable left-hand side on assignment; `-fno-realloc-lhs` turns it off.
## Self-check
Append to `s` in a loop and confirm `len(s)` equals the sum of piece lengths.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn page Arrays and strings (allocatable character strings, allocation on assignment, equal-length character arrays, `character(len=*)` dummy) and the gfortran Code Generation Options page (`-frealloc-lhs`). Removed: the old-gfortran bug note, the ragged-list advice and the claim that the F2003 default is the behaviour for every compiler, which no page read covers.
Method: documentation only; no commands were run.
