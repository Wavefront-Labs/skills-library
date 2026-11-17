---
id: computing-software.software-engineering.fortran.float-comparison
name: float-comparison
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, float-comparison, fortran-ieee]
level: practitioner
status: docs-checked
description: "Compare reals with absolute and relative tolerances using epsilon, not equality, and use -Wcompare-reals to find exact comparisons."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comparing floating-point numbers
**Goal:** compare floating values correctly.
```fortran
logical function close_to(a, b, rtol, atol)
  real(dp), intent(in) :: a, b
  real(dp), intent(in), optional :: rtol, atol
  real(dp) :: rt, at
  rt = 1.0e-9_dp; at = 1.0e-12_dp
  if (present(rtol)) rt = rtol
  if (present(atol)) at = atol
  close_to = abs(a - b) <= at + rt * max(abs(a), abs(b))
end function
```
- `-Wcompare-reals` (implied by `-Wextra`) warns when real or complex values are compared for equality or inequality.
- `epsilon(x)` returns the smallest number E of the same kind as X such that 1 + E > 1; scale it by magnitude and operation count to choose a tolerance.
- The tolerances above are examples; choose them from the problem's scale.
## Gotchas
- Tolerances depend on problem scale; do not hard-code one for all data.
- The `max` and `min` intrinsics do not specify behaviour when an argument is NaN; test with `ieee_is_nan` first.
## Self-check
Compile with `-Wextra` and confirm an `==` on reals warns.

## Checked
2026-11-02. Confirmed in the GNU Fortran manual: -Wcompare-reals implied by -Wextra, EPSILON definition, MAX/MIN NaN note (names IEEE_IS_NAN). Removed: the 0.1+0.2 binary-floating-point claim and its self-check (not on a page read).
Method: documentation only; no commands were run.
