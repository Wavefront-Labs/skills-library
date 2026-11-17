---
id: computing-software.software-engineering.fortran.error-stop-codes
name: error-stop-codes
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, error-stop-codes, fortran-error-handling]
level: practitioner
status: draft
description: "Terminate with error stop and integer codes, flush output, and return meaningful exit status to scripts."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://fortran-lang.org/learn/best_practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# error stop and exit codes
**Goal:** signal failure to callers.
```fortran
if (.not. ok) then
  write (error_unit, '(a)') 'fatal: config invalid'
  error stop 2
end if
```
- `error stop` with an integer sets the exit status (processor-dependent mapping; gfortran uses the value on common platforms); with a string it prints the message and exits nonzero.
- `stop 0` ends normally with status 0.
- Standard has no `exit` statement; `exit` is for loops. `call exit(n)` is a GNU extension.
- In `pure` procedures `error stop` is allowed (F2018).
## Gotchas
- Exit status values above 255 are truncated by the OS.
- Output buffers may not be flushed before `error stop` in some compilers; call `flush`.
## Self-check
Run in a shell and echo the status code.
