---
id: computing-software.software-engineering.fortran.environment-variables
name: environment-variables
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, environment-variables, fortran-cmdline-env]
level: practitioner
status: docs-checked
description: "Read environment variables with get_environment_variable and handle absence."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment variables
**Goal:** read configuration from the environment.
```fortran
character(len=255) :: val
integer :: n, stat
call get_environment_variable('HOME', val, length=n, status=stat)
if (stat == 0) print *, val(1:n)
```
- `get_environment_variable(name [, value, length, status, trim_name])`.
- If `value` is too short it is truncated; if the variable is not set `value` is filled with blanks and `length` is zero.
- `status` is -1 if `value` is present but too short, 1 if the variable does not exist, 2 if the processor does not support environment variables, otherwise zero.
- If `trim_name` is `.false.`, trailing blanks in `name` are significant.
## Gotchas
- The manual says `get_environment_variable` need not be thread-safe: do not update the environment concurrently with a call.
## Self-check
Query a variable that does not exist and verify `stat == 1`.

## Checked
2026-11-02. Confirmed in intrinsic.texi: GET_ENVIRONMENT_VARIABLE arguments, truncation, blank fill, status values -1/1/2, TRIM_NAME, thread-safety note. Removed: the two-step allocatable query, how to set variables (setenv/putenv), and the Windows USERPROFILE note (not on the pages read).
Method: documentation only; no commands were run.
