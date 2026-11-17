---
id: computing-software.software-engineering.fortran.direct-access
name: direct-access
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, direct-access, fortran-io-files]
level: advanced
status: draft
description: "Use access=direct with recl for fixed-size record files and understand sequential unformatted record markers."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Direct-access and sequential unformatted files
**Goal:** random access to fixed-size records.
```fortran
open (newunit=u, file='recs.dat', access='direct', form='unformatted', recl=64, status='replace')
write (u, rec=5) x
read  (u, rec=5) y
```
- `recl` units are processor-dependent (bytes in gfortran by default).
- Each READ/WRITE addresses one record by number.
- Sequential unformatted records have header and trailer length markers.
## Gotchas
- `recl` unit size differs across compilers (some use 4-byte words); check with `-assume byterecl` on Intel (unconfirmed flag name).
- Do not mix direct-access reading with differently-sized writes.
## Self-check
Write records 1..10 out of order, read each back, compare.
