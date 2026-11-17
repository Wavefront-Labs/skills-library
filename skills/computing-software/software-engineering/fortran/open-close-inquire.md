---
id: computing-software.software-engineering.fortran.open-close-inquire
name: open-close-inquire
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, open-close-inquire, fortran-io-files]
level: intro
status: draft
description: "Open files with newunit, status, action and iostat; inquire existence and size; close properly."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# open, close, inquire and units
**Goal:** handle files robustly.
```fortran
integer :: u, ios
character(len=256) :: msg
open (newunit=u, file='data.txt', status='old', action='read', iostat=ios, iomsg=msg)
if (ios /= 0) error stop trim(msg)
close (u)
inquire (file='out.txt', exist=found)
```
- `newunit=` (F2008) picks a free unit number; avoid hard-coded unit numbers.
- `status`: old, new, replace, scratch, unknown. `action`: read, write, readwrite. `position='append'`.
- `inquire(unit=u, size=s)` for file size in file storage units (unconfirmed per compiler; test).
## Gotchas
- Without `iostat`, a failed open aborts the program.
- Units 5, 6 (and 0 for stderr) are preconnected in gfortran; prefer `iso_fortran_env` names.
## Self-check
Open a missing file with `status='old'` and verify the message is printed.
