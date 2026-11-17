---
id: computing-software.software-engineering.fortran.stream-access
name: stream-access
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, stream-access, fortran-io-files]
level: advanced
status: draft
description: "Read and write binary data with access=stream and form=unformatted, avoiding record markers."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stream and unformatted access
**Goal:** do portable binary I/O.
```fortran
open (newunit=u, file='blob.bin', access='stream', form='unformatted', status='replace')
write (u) n, a(1:n)
rewind (u)
read (u) m
close (u)
```
- Stream access has no record markers; position with `pos=`.
- Default sequential unformatted files add record-length markers, which other languages cannot read directly.
- Endianness: gfortran `-fconvert=big-endian` or `convert=` on open (extension).
## Gotchas
- Binary files are not portable across kinds/endianness; document the format.
- Reading past the end sets `iostat` to a negative value (`iostat_end`).
## Self-check
Write 100 reals, read them back with stream access, and compare.
