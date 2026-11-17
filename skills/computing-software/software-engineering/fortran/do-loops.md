---
id: computing-software.software-engineering.fortran.do-loops
name: do-loops
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, do-loops, fortran-control-flow]
level: intro
status: gated
description: "Write counted do loops, do while, and unbounded do with exit; know loop variable and trip-count semantics."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# do loops and do while
**Goal:** loop correctly.
```fortran
do i = 1, n, 2          ! start, stop, step
  s = s + a(i)
end do
do while (err > tol)
  call step(err)
end do
do                       ! unbounded
  if (done) exit
end do
```
- The trip count is computed once before the loop: `max(0, (stop - start + step) / step)`. (gated: unconfirmed, source is paywalled or blocked)
- Do not modify the loop variable inside the body.
- After normal completion, the loop variable is `stop` rounded to the next step (e.g. `n+1` for step 1).
- Real loop variables were deleted from the standard; use integers.
## Gotchas
- `do i = n, 1` executes zero times (no negative step by default).
- Changing `n` inside the loop does not change the trip count.
## Self-check
Print `i` after `do i = 1, 3` completes; it is 4.

## Checked
2026-11-02. Confirmed: Nothing: only the fortran-lang arrays/strings quickstart was readable; the standard (J3) is not fetchable here.
Gated: whole skill; verify against the Fortran standard or compiler manual.
Method: documentation only; no commands were run.
