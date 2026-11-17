---
id: computing-software.software-engineering.fortran.do-concurrent
name: do-concurrent
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, do-concurrent, fortran-do-concurrent]
level: practitioner
status: draft
description: "Express independent loop iterations with do concurrent and know the restrictions that make it valid."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# do concurrent construct
**Goal:** tell the compiler iterations are independent.
```fortran
do concurrent (i = 1:n, j = 1:m)
  c(i, j) = a(i, j) + b(i, j)
end do
do concurrent (i = 1:n, mask(i) > 0)
  x(i) = sqrt(mask(i))
end do
```
- Iterations must not depend on each other and may run in any order; procedures called must be `pure`.
- No `exit` of the construct, no `return`, no image control statements.
- gfortran can parallelise it with `-ftree-parallelize-loops=N` (unconfirmed effectiveness; verify with `-fopt-info-loop`). nvfortran can offload it with `-stdpar`.
## Gotchas
- It is a promise, not a parallel directive; the compiler may run it serially.
- Reductions need the `reduce` locality spec (Fortran 2023); support varies by compiler (unconfirmed per release).
## Self-check
Compare results of the loop with an ordinary `do` over randomised iteration order.
