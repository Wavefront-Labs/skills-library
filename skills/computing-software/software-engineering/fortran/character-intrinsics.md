---
id: computing-software.software-engineering.fortran.character-intrinsics
name: character-intrinsics
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, character-intrinsics, fortran-strings]
level: intro
status: docs-checked
description: "Search and manipulate strings with len_trim, index, scan, verify, trim, adjustl, repeat and achar."
sources:
  - https://fortran-lang.org/learn/intrinsics/INDEX
  - https://fortran-lang.org/learn/intrinsics/SCAN
  - https://fortran-lang.org/learn/intrinsics/VERIFY
  - https://fortran-lang.org/learn/intrinsics/ACHAR
  - https://fortran-lang.org/learn/intrinsics/TRIM
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Character intrinsics
**Goal:** do common string tasks.
```fortran
s = '  Hello, World'
print *, index(s, 'World')         ! position of substring
print *, scan(s, ',;')             ! first of any characters
print *, verify(s, 'abc ')         ! first char not in set
print *, trim(adjustl(s))          ! 'Hello, World'
print *, repeat('-', 20), achar(65), iachar('A')
```
- Concatenate with `//`; strings in a `character` array are truncated or right-padded with blanks to the declared length, so use `trim` when printing.
- `index(s, sub, back=.true.)` finds the last occurrence.
## Gotchas
- There is no case-conversion intrinsic; the `achar` page builds an `upper` function from `iachar` and `achar`.
- `index` is case-sensitive and returns 0 when the substring is not found.
## Self-check
Verify `index('abcabc', 'c', back=.true.)` returns 6.

## Checked
2026-11-03. Confirmed against the fortran-lang.org intrinsic pages for `index`, `scan`, `verify`, `trim`, `adjustl`, `repeat`, `achar` and `iachar` and the Arrays and strings page (concatenation, padding): leftmost and `back` rightmost semantics, trailing-blank removal, the `upper` example. Removed: substring slice rules, comparison and trailing-blank rule, `stdlib` `to_upper`, and the `-fcheck=bounds` substring claim (the gfortran page says substring checking is not currently included).
Method: documentation only; no commands were run.
