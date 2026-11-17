---
id: computing-software.software-engineering.fortran.internal-io
name: internal-io
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, internal-io, fortran-io-formatted]
level: practitioner
status: draft
description: "Convert between numbers and strings using write and read on character variables."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Internal I/O on strings
**Goal:** format and parse text without external files.
```fortran
character(len=32) :: buf
integer :: n, ios
write (buf, '(i0)') 42                ! number to string
read (buf, *, iostat=ios) n           ! string to number
if (ios /= 0) print *, 'bad integer'
```
- A character scalar is one record; an array of strings is multiple records.
- Use `iostat` to detect conversion failure.
- A deferred-length string can be sized after measuring (write to a big buffer, then `trim`).
## Gotchas
- Writing more characters than the buffer holds raises a runtime error.
- `adjustl` and `trim` clean up padded results.
## Self-check
Feed `'abc'` to the integer read and confirm `ios /= 0`.
