---
id: computing-software.software-engineering.fortran.fortran-2023-features
name: fortran-2023-features
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, fortran-2023-features, fortran-standards]
level: advanced
status: draft
description: "Use select Fortran 2023 features such as the trig degree functions, conditional expressions, and enumeration types where compilers support them."
sources:
  - https://j3-fortran.org/
  - https://wg5-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fortran 2023 additions
**Goal:** adopt new features cautiously.
- Fortran 2023 (ISO/IEC 1539-1:2023) is a minor revision. Items commonly cited (unconfirmed list, verify against the published standard): `split` and `tokenize` string intrinsics, `out_of_range`, degree-based trigonometric functions (`sind`, `cosd`, `tand`), conditional expressions `( cond ? a : b )`, enumeration types, and `reduce` in `do concurrent`. Generic programming (templates) was deferred to a later revision.
- Treat each as unconfirmed for your compiler until you test it; gfortran support is incremental per release.
- Check feature tables in the gfortran manual or compiler release notes.
## Gotchas
- Do not use these in code that must build on older compilers.
- J3 papers and drafts may differ from the final text; use the published standard.
## Self-check
Compile a one-line `sind(30.0)` test with `-std=f2023` to see if your compiler accepts it.
