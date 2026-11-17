---
id: computing-software.software-engineering.fortran.exit-cycle-named
name: exit-cycle-named
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, exit-cycle-named, fortran-control-flow]
level: practitioner
status: gated
description: "Use exit and cycle with named do, if, and block constructs to leave nested loops without goto."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# exit, cycle and named constructs
**Goal:** control nested loops cleanly.
```fortran
outer: do i = 1, n
  inner: do j = 1, m
    if (a(i, j) < 0) cycle outer       ! next i
    if (a(i, j) > 100) exit outer      ! leave both loops
  end do inner
end do outer
```
- Any construct can be named (`name: if (...) then ... end if name`); the end name must match. (gated: unconfirmed, source is paywalled or blocked)
- `exit` can leave `block`, `if`, `select case` constructs by name (F2008).
- `block ... end block` creates a scope for local declarations.
## Gotchas
- `exit` without a name leaves only the innermost `do`.
- Labels and construct names are different namespaces from variables; avoid reusing identifiers anyway.
## Self-check
Verify that `exit outer` skips remaining `i` iterations.

## Checked
2026-11-02. Confirmed: Nothing: only the fortran-lang arrays/strings quickstart was readable; the standard (J3) is not fetchable here.
Gated: whole skill; verify against the Fortran standard or compiler manual.
Method: documentation only; no commands were run.
