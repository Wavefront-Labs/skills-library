---
id: computing-software.software-engineering.fortran.bind-c-procedures
name: bind-c-procedures
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, bind-c-procedures, fortran-c-interop]
level: practitioner
status: docs-checked
description: "Call C from Fortran with bind(c, name=...) interfaces, value arguments, C strings and gfortran name mangling."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bind(c) procedures
**Goal:** cross-call without mangling issues.
Fortran calling C `double add(double a, double b)`:
```fortran
interface
  function add(a, b) bind(c, name='add') result(r)
    import :: c_double
    real(c_double), value :: a, b
    real(c_double) :: r
  end function
end interface
```
- Subroutines and functions need the `BIND(C)` attribute to be compatible with C. C passes by value by default and Fortran by reference, so use `VALUE` for by-value arguments; pointer arguments often need `VALUE` too.
- Strings: C strings are NUL terminated; declare `character(kind=c_char) :: string(*)` (a length-one assumed-size array); `character(len=*)` is not allowed. Pass `c_char_"text"//c_null_char`.
- Without `BIND(C)`, the default procedure name is the lowercased Fortran name with an appended underscore (`-fno-underscoring` removes it, `-fsecond-underscore` appends two); module procedures are named `__<module>_MOD_<name>`.
- `-fc-prototypes` writes C declarations for `BIND(C)` entities.
## Self-check
Link a small C and Fortran pair and verify the numerical result.

## Checked
2026-11-02. Confirmed in gfortran.texi: BIND(C) requirement, VALUE, string rules (assumed-size char array, NUL termination), default name mangling and -fno-underscoring/-fsecond-underscore, __module_MOD_name, -fc-prototypes. Removed: the C-calling-Fortran example, 'arrays stay by reference' wording, and binding-label claim beyond the manual.
Method: documentation only; no commands were run.
