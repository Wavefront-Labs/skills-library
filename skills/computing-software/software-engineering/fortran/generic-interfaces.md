---
id: computing-software.software-engineering.fortran.generic-interfaces
name: generic-interfaces
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, generic-interfaces, fortran-generic]
level: practitioner
status: draft
description: "Create generic names over specific procedures with interface blocks in modules so calls resolve by argument type, kind and rank."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generic procedure interfaces
**Goal:** provide one name for several implementations.
```fortran
interface swap
  module procedure swap_int, swap_real
end interface
```
- Specifics must be distinguishable by type/kind/rank of non-optional dummy arguments.
- `module procedure` lists module procedures; for external or procedure-pointer specifics use `procedure`.
- Intrinsic names can be extended: a generic named like an intrinsic adds specifics without hiding it.
- Type-bound generics: `generic :: write(formatted) => ...` (see operators).
## Gotchas
- Ambiguous specifics are diagnosed at definition time, not at call time.
- Distinguishing only by `intent` or by name of dummies is not allowed; keywords alone do not disambiguate.
## Self-check
Call `swap` with integers and with reals and confirm each specific runs.
