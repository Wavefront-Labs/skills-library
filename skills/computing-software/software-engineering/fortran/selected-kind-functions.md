---
id: computing-software.software-engineering.fortran.selected-kind-functions
name: selected-kind-functions
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, selected-kind-functions, fortran-kinds]
level: practitioner
status: docs-checked
description: "Request precision or range with selected_real_kind and selected_int_kind and handle the negative return when unsupported."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# selected_real_kind and selected_int_kind
**Goal:** request numeric properties rather than sizes.
- `selected_real_kind([p, r, radix])` returns the kind of a real type with decimal precision of at least `p` digits, decimal exponent range of at least `r` and the requested radix; if more than one kind qualifies, the one with the smallest decimal precision is returned. Since Fortran 2008 absent `p` or `r` are taken as zero; `radix` is Fortran 2008.
- `selected_int_kind(r)` returns the kind of the smallest integer type that can represent all values from -10^r to 10^r (exclusive), or -1 if there is none.
- When no real kind matches, `selected_real_kind` returns -1 (precision not supported), -2 (exponent range not supported), -3 (only `radix` can be met), -4 (`radix` and one of `p` or `r` can be met) or -5 (no real type with that `radix`).
```fortran
integer, parameter :: dp = selected_real_kind(15, 307)
integer, parameter :: i9 = selected_int_kind(9)
real(dp) :: x
```
- `selected_char_kind(name)` returns the kind for the named character set, or -1; supported names include `'ASCII'` and `'DEFAULT'` (equivalent) and `'ISO_10646'` (UCS-4, Unicode).
- `precision(x)`, `range(x)`, `epsilon(x)`, `tiny(x)`, `huge(x)` and `kind(x)` inquire about a value's model.
## Self-check
Print `precision(1.0_dp)` and confirm it is at least 15.

## Checked
2026-11-02. Confirmed in intrinsic.texi: SELECTED_REAL_KIND (smallest precision rule, R/P optional since F2008, RADIX F2008, return values -1..-5), SELECTED_INT_KIND, SELECTED_CHAR_KIND names, PRECISION, RANGE, EPSILON, TINY, HUGE. Removed: 'compile error when used as kind' claim.
Method: documentation only; no commands were run.
