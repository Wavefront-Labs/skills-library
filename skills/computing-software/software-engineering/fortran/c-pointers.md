---
id: computing-software.software-engineering.fortran.c-pointers
name: c-pointers
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, c-pointers, fortran-c-interop]
level: advanced
status: docs-checked
description: "Convert between Fortran arrays and C pointers with c_loc, c_f_pointer and c_associated."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# c_ptr, c_loc and c_f_pointer
**Goal:** share memory with C code.
```fortran
type(c_ptr) :: cp
real(c_double), pointer :: arr(:)
call c_f_pointer(cp, arr, [n])      ! view C memory as a Fortran array
cp = c_loc(arr(1))                  ! arr needs the target or pointer attribute
if (.not. c_associated(cp)) error stop
```
- `c_f_pointer(cptr, fptr [, shape, lower])` assigns the target of the C pointer to the Fortran pointer; `shape` must be present if and only if `fptr` is an array; `lower` (Fortran 2023) gives lower bounds.
- `c_loc(x)`: `x` must have the `pointer` or `target` attribute and must not be a coindexed object; the result is a `c_ptr`.
- `c_associated(cptr1 [, cptr2])` is false if `cptr1` is a C NULL pointer or the two point to different addresses.
- `c_funloc` gives the address of an interoperable function as a `c_funptr`; `c_f_procpointer(cptr, fptr)` assigns a C function pointer to a Fortran procedure pointer.
- Strings passed to C must be NUL terminated (`c_null_char`).
## Gotchas
- The C side owns memory it allocated; do not `deallocate` a pointer you did not allocate in Fortran.
## Self-check
Receive an array pointer from C, view it with `c_f_pointer`, sum it, and free it on the C side.

## Checked
2026-11-02. Confirmed in intrinsic.texi: C_F_POINTER (shape rule, LOWER is Fortran 2023), C_LOC requirements, C_ASSOCIATED result, C_FUNLOC, C_F_PROCPOINTER; gfortran.texi for NUL-terminated strings. Removed: character-array loop idiom and deallocate-lifetime wording beyond what is stated.
Method: documentation only; no commands were run.
