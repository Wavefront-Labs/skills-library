---
id: computing-software.software-engineering.fortran.parameterized-derived-types
name: parameterized-derived-types
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, parameterized-derived-types, fortran-derived-types]
level: advanced
status: draft
description: "Use kind and len type parameters on derived types, and know that compiler support is uneven."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parameterized derived types
**Goal:** write generic containers by kind or length.
```fortran
type :: matrix(k, n)
  integer, kind :: k = kind(1.0)
  integer, len  :: n
  real(k) :: a(n, n)
end type
type(matrix(k=8, n=3)) :: m
```
- `kind` parameters are compile-time; `len` parameters may be set at run time.
- Inquiry: `m%n`, `m%k`.
## Gotchas
- Support in compilers has historically been incomplete or buggy; test your exact gfortran/ifx/flang version before relying on PDTs (unconfirmed current status, verify per release notes).
- For simple needs prefer modules plus kind constants.
## Self-check
Compile the example with `-std=f2018` on your target compiler; if it ICEs or errors, fall back to non-PDT design.
