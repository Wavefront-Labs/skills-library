---
id: computing-software.software-engineering.fortran.main-program
name: main-program
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, main-program, fortran-modules]
level: intro
status: draft
description: "Structure a main program and choose between stop, error stop and return codes for termination."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://fortran-lang.org/learn/best_practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Main program and stop statements
**Goal:** end programs with correct exit status.
```fortran
program app
  use, intrinsic :: iso_fortran_env, only: error_unit
  implicit none
  integer :: ierr
  call run(ierr)
  if (ierr /= 0) then
    write (error_unit, '(a)') 'failed'
    error stop 1
  end if
end program app
```
- `stop` ends normally (exit status 0 unless a code given: `stop 2`); `error stop` signals error termination (nonzero exit status; gfortran returns the given code).
- `call exit(n)` is a common GNU extension, not standard; `stop n` is standard.
- Output on `stop` may print the code to stderr depending on the compiler.
## Gotchas
- `error stop` in a coarray program stops all images.
- Buffered output may be lost on abnormal termination; `flush(unit)` first.
## Self-check
Run the example and check the shell exit status with `echo $?`.
