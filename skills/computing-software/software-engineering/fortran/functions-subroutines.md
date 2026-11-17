---
id: computing-software.software-engineering.fortran.functions-subroutines
name: functions-subroutines
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, functions-subroutines, fortran-procedures]
level: intro
status: draft
description: "Write functions with result clauses and subroutines with call, understanding argument association by reference."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://fortran-lang.org/learn/best_practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Functions, subroutines and result
**Goal:** structure code into procedures.
```fortran
pure function norm1(v) result(r)
  real, intent(in) :: v(:)
  real :: r
  r = sum(abs(v))
end function
subroutine swap(a, b)
  real, intent(inout) :: a, b
  real :: t
  t = a; a = b; b = t
end subroutine
```
- Arguments are passed by reference; `intent` documents direction.
- Put procedures inside modules (`contains`) so interfaces are explicit.
- Functions return a value via the result variable; side effects are legal unless `pure`.
## Gotchas
- An external procedure without an interface gets no argument checking.
- A function without `result` returns via a variable named like the function; use `result` for recursion.
## Self-check
Compile with `-Wall -fcheck=all` and confirm no implicit-interface warnings.
