---
id: computing-software.software-engineering.fortran.array-constructors
name: array-constructors
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, array-constructors, fortran-arrays-basics]
level: intro
status: gated
description: "Build arrays with [ ] constructors, implied do loops, type-spec prefix and reshape."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Array constructors
**Goal:** initialise arrays declaratively.
```fortran
integer :: v(5) = [1, 2, 3, 4, 5]
real    :: x(10)
x = [(real(i)**2, i = 1, 10)]            ! implied do
character(len=3) :: s(2) = [character(len=3) :: 'a', 'bcd']
```
- F2003 allows `[` `]` in place of `(/` `/)`. (gated: unconfirmed, source is paywalled or blocked)
- A type-spec (`[real :: 1, 2]`) sets the type and kind of all elements.
- For 2-D, build with `reshape([...], [2, 3])`.
## Gotchas
- Elements of different character lengths without a type-spec are a standard violation in F2003 before type-spec; use the type-spec form.
- The loop variable of an implied do must be a declared integer.
## Self-check
Print `sum([(i, i=1,100)])`; expect 5050.

## Checked
2026-11-02. Confirmed: Nothing: only the fortran-lang arrays/strings quickstart was readable; the standard (J3) is not fetchable here.
Gated: whole skill; verify against the Fortran standard or compiler manual.
Method: documentation only; no commands were run.
