---
id: computing-software.software-engineering.fortran.iso-c-binding
name: iso-c-binding
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, iso-c-binding, fortran-c-interop]
level: practitioner
status: docs-checked
description: "Use c_int, c_double, c_char and other kind constants from iso_c_binding to match C types."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iso_c_binding kinds and types
**Goal:** match C types exactly.
```fortran
use, intrinsic :: iso_c_binding
integer(c_int) :: n
real(c_double) :: x
character(kind=c_char) :: ch
```
- Named constants of default integer kind, usable as KIND parameters: `c_int` (int), `c_short`, `c_long` (long int), `c_long_long`, `c_signed_char`, `c_size_t` (size_t), `c_intptr_t`, `c_float` (float), `c_double` (double), `c_long_double` (long double), `c_float_complex`, `c_double_complex`, `c_bool` (_Bool), `c_char` (char).
- The module also provides `c_associated`, `c_f_pointer`, `c_f_procpointer`, `c_funloc`, `c_loc` and `c_sizeof`.
- C `_Bool` true is 1 and false 0; using other integer values with a Fortran `logical` gives an undefined result.
- Use `c_null_char` to terminate C strings.
## Gotchas
- For C interoperability use the `iso_c_binding` kinds, not default kinds or literal kind numbers.
## Self-check
Print `c_int` and `c_double`; they are kind values for your compiler.

## Checked
2026-11-02. Confirmed in intrinsic.texi (ISO_C_BINDING table of named constants and the procedure list) and gfortran.texi (logical/_Bool values, NUL termination, use C kinds). Removed: c_ptr is void*/c_funptr mapping, c_null_ptr, 'negative value' claim for unsupported kinds, kind-value self-check expectation (not stated).
Method: documentation only; no commands were run.
