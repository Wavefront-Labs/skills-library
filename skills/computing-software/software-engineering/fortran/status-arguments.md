---
id: computing-software.software-engineering.fortran.status-arguments
name: status-arguments
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, status-arguments, fortran-error-handling]
level: practitioner
status: draft
description: "Design procedures that return status via optional stat and errmsg arguments or result types instead of stopping inside libraries."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://fortran-lang.org/learn/best_practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# stat and errmsg patterns
**Goal:** let callers decide how to fail.
```fortran
subroutine load(file, data, stat, errmsg)
  character(len=*), intent(in) :: file
  real, allocatable, intent(out) :: data(:)
  integer, intent(out), optional :: stat
  character(len=*), intent(out), optional :: errmsg
  integer :: ios
  open (newunit=u, file=file, status='old', iostat=ios)
  if (ios /= 0) then
    if (present(stat)) then
      stat = ios
      if (present(errmsg)) errmsg = 'cannot open '//file
      return
    else
      error stop 'cannot open file'
    end if
  end if
```
- Library code returns errors; applications decide to `error stop`.
- Mirror the intrinsic pattern (`allocate(..., stat=, errmsg=)`) and the `stat`/`errmsg` style of F2008 intrinsics.
- Alternative: an `error_type` derived type allocated on failure (as in test-drive / stdlib).
## Gotchas
- If the caller omits `stat`, abort so errors are never silently dropped.
- `errmsg` shorter than the message is truncated.
## Self-check
Call with and without `stat` for a missing file and see both behaviours.
