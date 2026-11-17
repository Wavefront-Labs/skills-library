---
id: computing-software.software-engineering.fortran.test-drive
name: test-drive
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, test-drive, fortran-testing]
level: practitioner
status: draft
description: "Write unit tests with the test-drive framework, register suites, and run them via fpm test."
sources:
  - https://github.com/fortran-lang/test-drive
  - https://github.com/Goddard-Fortran-Ecosystem/pFUnit
  - https://fpm.fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# test-drive unit testing with fpm
**Goal:** automate tests in Fortran.
```fortran
module test_geom
  use testdrive, only: new_unittest, unittest_type, error_type, check
  implicit none
  private
  public :: collect_geom
contains
  subroutine collect_geom(testsuite)
    type(unittest_type), allocatable, intent(out) :: testsuite(:)
    testsuite = [new_unittest('area', test_area)]
  end subroutine
  subroutine test_area(error)
    type(error_type), allocatable, intent(out) :: error
    call check(error, abs(area(1.0) - 3.14159) < 1e-4, 'area of unit circle')
    if (allocated(error)) return
  end subroutine
end module
```
- Add `test-drive` as a `dev-dependency`, a `test/main.f90` that calls `run_testsuite` with `collect_geom`, then `fpm test`.
- Exit code is nonzero on failure, suitable for CI.
## Gotchas
- Exact helper names (`check`, `run_testsuite`) follow the test-drive README; verify against the version you pin.
- Test modules and main driver need consistent suite names.
## Self-check
Break the expected value and confirm `fpm test` fails.
