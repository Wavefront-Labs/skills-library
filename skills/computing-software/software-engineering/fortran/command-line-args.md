---
id: computing-software.software-engineering.fortran.command-line-args
name: command-line-args
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, command-line-args, fortran-cmdline-env]
level: intro
status: docs-checked
description: "Read arguments with command_argument_count and get_command_argument."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Command-line arguments
**Goal:** write CLI programs.
```fortran
integer :: n, i, stat, alen
character(len=256) :: buf
n = command_argument_count()
do i = 1, n
  call get_command_argument(i, buf, length=alen, status=stat)
  print *, i, buf(1:alen)
end do
```
- `get_command_argument(number [, value, length, status])`: `number` 0 gives the program name (on systems that support it); `value` is truncated to fit and `status` is -1 in that case, positive if retrieval fails, otherwise zero; `length` is the length of the argument.
- `get_command([command, length, status])` returns the entire command line; `status` is 0 on success, -1 if `command` is too short, positive on error.
- `command_argument_count()` returns the number of arguments.
## Gotchas
- A fixed buffer truncates long arguments; check `status` (-1) or compare `length` with the buffer length.
- If there are fewer than `number` arguments, `value` is filled with blanks.
## Self-check
Run with 3 arguments and confirm the count is 3.

## Checked
2026-11-02. Confirmed in intrinsic.texi: GET_COMMAND_ARGUMENT (arguments, number 0, truncation, status values, length), GET_COMMAND (status values), COMMAND_ARGUMENT_COUNT. Removed: internal-read advice and the allocatable-string loop (not on the pages read).
Method: documentation only; no commands were run.
