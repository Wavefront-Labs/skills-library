---
id: computing-software.software-engineering.fortran.c-interop-types
name: c-interop-types
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, c-interop-types, fortran-c-interop]
level: sme
status: docs-checked
description: "Define bind(c) derived types matching C structs, and handle assumed-shape arrays across the language boundary with ISO_Fortran_binding.h."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interoperable derived types and descriptors
**Goal:** pass structs and descriptors.
```fortran
type, bind(c) :: vec3
  real(c_double) :: x, y, z
end type
```
- To be compatible with a C `struct`, use the `BIND(C)` attribute in the type declaration; the manual's example uses `INTEGER(C_INT)`, `REAL(C_DOUBLE)`, `CHARACTER(KIND=C_CHAR)` components.
- The Fortran 2018 / TS 29113 features add assumed-type (`TYPE(*)`) and assumed-rank (`DIMENSION(..)`) and allow interoperability of assumed-shape, assumed-rank, deferred-shape arrays, allocatables and pointers; such objects reach `BIND(C)` functions as descriptors declared in `<ISO_Fortran_binding.h>`.
- GNU Fortran converts arguments of `BIND(C)` functions to that standard descriptor; its internal descriptor for other functions has different fields.
## Gotchas
- Component restrictions for `bind(c)` types are defined by the Fortran standard; confirm them there.
## Self-check
Declare the type, write the matching C struct, and compare their sizes with a test program.

## Checked
2026-11-02. Confirmed in gfortran.texi: BIND(C) derived type vs struct, TS 29113 features and ISO_Fortran_binding.h, descriptor conversion note. Removed: CFI_cdesc_t / CFI_establish names, component restrictions, padding and storage_size comparison (not on the pages read).
Method: documentation only; no commands were run.
