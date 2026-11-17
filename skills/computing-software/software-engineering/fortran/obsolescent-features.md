---
id: computing-software.software-engineering.fortran.obsolescent-features
name: obsolescent-features
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, obsolescent-features, fortran-legacy]
level: practitioner
status: draft
description: "Identify arithmetic if, computed goto, assigned goto, shared do termination, and other obsolescent or deleted features and their modern replacements."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://fortran-lang.org/learn/best_practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Obsolescent and deleted features
**Goal:** recognise outdated constructs.
- Deleted in F95: real/double loop variables, `pause`, assigned `goto` and `assign`, the `H` edit descriptor. F2018 additionally deleted arithmetic `if` and non-block `do` (unconfirmed; check Annex B).
- Obsolescent: computed `goto` -> `select case`, `forall` -> `do concurrent`, `common` and `equivalence` -> modules, alternate return, statement functions.
- Compiler flags: `gfortran -std=f2018 -Wall` flags use of extensions and deleted features; `-std=legacy` accepts old code.
```fortran
! old: IF (X) 10, 20, 30
! new:
if (x < 0.0) then
  ...
else if (x == 0.0) then
  ...
else
  ...
end if
```
## Gotchas
- Warnings are compiler-specific; read the standard's annex B for the full list.
- `-std=f2018` rejects widely used extensions such as `real*8`.
## Self-check
Compile an old file with `-std=f2018` and list errors by category.
