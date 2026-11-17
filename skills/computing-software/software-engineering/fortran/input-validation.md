---
id: computing-software.software-engineering.fortran.input-validation
name: input-validation
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, input-validation, fortran-security]
level: practitioner
status: draft
description: "Validate input read from files and the command line: check iostat, ranges and sizes before allocating or indexing."
sources:
  - https://gcc.gnu.org/onlinedocs/gfortran/
  - https://gcc.gnu.org/onlinedocs/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Validating external input
**Goal:** avoid crashes and exploitation from untrusted data.
```fortran
read (u, *, iostat=ios) n
if (ios /= 0 .or. n < 0 .or. n > max_n) then
  error stop 'invalid n'
end if
allocate(a(n), stat=ios)
if (ios /= 0) error stop 'allocation failed'
```
- Check every `read`, `open`, `allocate` status; bound sizes from files before allocation.
- Reject negative or huge sizes; validate indices against `size()`.
- Avoid `execute_command_line` with untrusted strings (shell injection).
- Use `character(len=*)` with `len_trim` limits; avoid fixed buffers silently truncating names or paths.
## Gotchas
- `read(*,*)` list-directed accepts many odd forms (slashes, repeats); parse strictly when security matters.
- Integer overflow in size computations (`n*m`) wraps silently; use `int64` and check.
## Self-check
Feed malformed and oversized values and verify the program rejects them cleanly.
