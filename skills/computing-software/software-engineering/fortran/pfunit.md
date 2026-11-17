---
id: computing-software.software-engineering.fortran.pfunit
name: pfunit
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, pfunit, fortran-testing]
level: advanced
status: draft
description: "Write tests with pFUnit's preprocessed test files and run them under CMake, including MPI and parameterised tests."
sources:
  - https://github.com/fortran-lang/test-drive
  - https://github.com/Goddard-Fortran-Ecosystem/pFUnit
  - https://fpm.fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# pFUnit testing
**Goal:** use the xUnit-style Fortran framework.
```fortran
@test
subroutine test_add()
  use pfunit
  @assertEqual(4, add(2, 2))
end subroutine
```
- pFUnit (Goddard Fortran Ecosystem) uses a Python-based preprocessor to turn `.pf` files into Fortran; builds with CMake.
- Supports MPI-parallel tests and parameterised tests.
- Heavier setup than test-drive; best for large HPC codes.
- Check the pFUnit repository for the current assertion macros and version requirements (the example is indicative).
## Gotchas
- Preprocessor requires Python and specific CMake setup.
- Mixing compilers between pFUnit and your code leads to `.mod` mismatches.
## Self-check
Run one passing and one failing test and view the report.
