---
id: computing-software.software-engineering.fortran.use-only-rename
name: use-only-rename
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, use-only-rename, fortran-modules]
level: practitioner
status: draft
description: "Import precisely with use module, only: names and rename on clash with local => remote."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://fortran-lang.org/learn/best_practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# use association with only and rename
**Goal:** control namespaces.
```fortran
use geometry, only: area
use other, only: area2 => area         ! rename on clash
use, intrinsic :: iso_c_binding, only: c_int
use, non_intrinsic :: mymod
```
- `only:` limits visible names; omit it only for small modules.
- Renaming applies only in the importing scope.
- Operators: `use m, only: operator(+), assignment(=)`.
## Gotchas
- Two imports with the same name are only an error if the name is referenced.
- `only:` with no list is legal (imports nothing but ordering/side effects).
## Self-check
Import the same name from two modules with a rename and print both.
