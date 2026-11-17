---
id: computing-software.software-engineering.fortran.iostat-iomsg
name: iostat-iomsg
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, iostat-iomsg, fortran-error-handling]
level: practitioner
status: draft
description: "Handle I/O failures with iostat, iomsg and the iostat_end / iostat_eor constants."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://fortran-lang.org/learn/best_practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# iostat, iomsg and err handling in I/O
**Goal:** make I/O errors recoverable.
```fortran
use, intrinsic :: iso_fortran_env, only: iostat_end
character(len=256) :: msg
do
  read (u, *, iostat=ios, iomsg=msg) x
  if (ios == iostat_end) exit
  if (ios /= 0) then
    print *, 'read error: ', trim(msg)
    exit
  end if
end do
```
- `iostat` is 0 on success, negative on end-of-file/record, positive on error.
- Without `iostat`, `err` or `end`, an I/O error aborts the program.
- `is_iostat_end(ios)` and `is_iostat_eor(ios)` (F2003) are standard tests.
## Gotchas
- Specifying `iostat` suppresses abort even for errors you forgot to test.
- Message text is processor-dependent.
## Self-check
Read until EOF from an empty file and confirm the loop exits cleanly.
