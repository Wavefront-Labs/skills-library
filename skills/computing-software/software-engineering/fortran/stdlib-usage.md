---
id: computing-software.software-engineering.fortran.stdlib-usage
name: stdlib-usage
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, stdlib-usage, fortran-stdlib]
level: practitioner
status: draft
description: "Add the community Fortran standard library via fpm or CMake and use modules such as stdlib_kinds, stdlib_error and stdlib_ascii."
sources:
  - https://stdlib.fortran-lang.org/
  - https://fpm.fortran-lang.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Using stdlib in a project
**Goal:** use well-tested library code.
```toml
[dependencies]
stdlib = "*"
```
```fortran
use stdlib_kinds, only: dp, int64
use stdlib_ascii, only: to_upper
use stdlib_error, only: check
call check(n > 0, msg='n must be positive')
```
- Documentation at stdlib.fortran-lang.org lists modules, e.g. `stdlib_kinds`, `stdlib_ascii`, `stdlib_strings`, `stdlib_sorting`, `stdlib_stats`, `stdlib_linalg`, `stdlib_io`, `stdlib_hashmaps`, `stdlib_specialfunctions`.
- Many features track the J3-adopted wishlist; some modules are experimental.
- Build from source via CMake (`BUILD_SHARED_LIBS`) or fpm; conda-forge provides binaries.
## Gotchas
- Module API and names can change between stdlib releases; pin a version.
- Not everything in the documentation is present in every release; check the version.
## Self-check
Compile a program that calls `to_upper('abc')` and prints ABC.
