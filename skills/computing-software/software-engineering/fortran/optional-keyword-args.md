---
id: computing-software.software-engineering.fortran.optional-keyword-args
name: optional-keyword-args
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, optional-keyword-args, fortran-procedures]
level: practitioner
status: docs-checked
description: "Declare optional dummy arguments, test with present, and call with keyword arguments for readable calls."
sources:
  - https://fortran-lang.org/learn/best_practices/allocatable_arrays
  - https://fortran-lang.org/learn/quickstart/organising_code
  - https://fortran-lang.org/learn/intrinsics/CSHIFT
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optional and keyword arguments
**Goal:** build flexible procedure interfaces.
```fortran
subroutine solve(a, b, tol, maxit)
  real, intent(in) :: a(:, :), b(:)
  real, intent(in), optional :: tol
  integer, intent(in), optional :: maxit
  real :: t
  t = 1.0e-6
  if (present(tol)) t = tol
end subroutine
call solve(a, b, maxit=50)
```
- Put the procedure in a module: modules generate the explicit interfaces that modern procedure features need.
- Test an optional dummy with `present(name)` before using it.
- An unallocated allocatable actual argument is treated as not present when passed to an `optional` dummy.
- Keyword arguments work on intrinsics too, e.g. `cshift(a, shift=1, dim=2)`.
## Gotchas
- Use an optional dummy only after a `present` test, as the `resize` example does with `present(n)`.
## Self-check
Call with and without `tol` and confirm each path.

## Checked
2026-11-03. Confirmed against the fortran-lang.org Learn pages Allocatable Arrays (`optional`, `present`, unallocated actual not present), Organising code structure (module-generated interfaces) and the `cshift` intrinsic page (keyword arguments). Removed: the keyword-ordering rule, the absent-argument pass-through rule and the optional `intent(out)` note, which no page read covers.
Method: documentation only; no commands were run.
