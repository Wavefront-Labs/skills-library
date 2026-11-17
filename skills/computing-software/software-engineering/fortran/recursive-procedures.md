---
id: computing-software.software-engineering.fortran.recursive-procedures
name: recursive-procedures
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, recursive-procedures, fortran-procedures]
level: practitioner
status: draft
description: "Declare recursive procedures explicitly, use result for recursive functions, and watch stack depth."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://fortran-lang.org/learn/best_practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# recursive procedures
**Goal:** write recursion that compiles and is safe.
```fortran
recursive function fact(n) result(r)
  integer, intent(in) :: n
  integer(8) :: r
  if (n <= 1) then
    r = 1
  else
    r = n * fact(n - 1)
  end if
end function
```
- Since F2018, procedures are recursive by default unless `non_recursive`; before F2018 you needed `recursive`.
- gfortran `-frecursive` forces locals on the stack; `-fopenmp` implies it.
- Deep recursion with large locals can overflow the stack; use `ulimit -s` or heap arrays.
## Gotchas
- A recursive function needs `result(...)` if the function name is used as a variable on the left side.
- Implicit save variables break recursion (see the save skill).
## Self-check
Compute `fact(10)` and verify 3628800.
