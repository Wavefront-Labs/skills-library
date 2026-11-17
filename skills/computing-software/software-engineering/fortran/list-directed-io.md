---
id: computing-software.software-engineering.fortran.list-directed-io
name: list-directed-io
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, list-directed-io, fortran-io-formatted]
level: intro
status: draft
description: "Use print * and read * for quick I/O and understand separators, null values and quirks."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# List-directed I/O
**Goal:** use list-directed I/O appropriately.
```fortran
read (*, *) n, x
print *, 'sum =', n + x
write (unit, *) a      ! list-directed to a file unit
```
- Fields separated by blank, comma or slash; `/` ends the read leaving remaining variables unchanged.
- Repeat counts: `3*0.0` supplies three values.
- Character input without quotes stops at blanks.
- Output formatting (widths, leading blank) is processor-dependent.
## Gotchas
- Do not use it for exact output formats consumed by other programs.
- `read(*,*)` of a char var with a comma-bearing string needs quotes.
## Self-check
Pipe `echo "3 4.5" | ./prog` and verify the parsed values.
