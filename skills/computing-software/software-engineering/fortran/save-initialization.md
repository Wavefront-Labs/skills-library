---
id: computing-software.software-engineering.fortran.save-initialization
name: save-initialization
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, save-initialization, fortran-declarations]
level: practitioner
status: draft
description: "Understand that initialising a local variable in its declaration implies save, and use save and local state deliberately."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://fortran-lang.org/learn/best_practices/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# save attribute and initial values
**Goal:** avoid accidental persistent state.
- `integer :: count = 0` in a procedure implies `save`: the value persists between calls and is initialised once.
- `integer :: count; count = 0` is reset on each call.
- Module variables are implicitly saved in F2008 and later.
```fortran
subroutine tick()
  integer :: n = 0        ! implicitly saved
  n = n + 1
  print *, n
end subroutine
```
## Gotchas
- Implicit save makes procedures non-reentrant and unsafe in OpenMP; gfortran `-fmax-stack-var-size` and `-frecursive` interact with this.
- `pure`, `elemental` and `recursive` procedures cannot hold saved variables that are modified.
## Self-check
Call `tick` three times and confirm 1, 2, 3; then move the initialisation to an assignment and confirm 1, 1, 1.
