---
id: computing-software.software-engineering.fortran.coarray-teams-events
name: coarray-teams-events
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, coarray-teams-events, fortran-coarrays]
level: sme
status: draft
description: "Partition images with form team and change team, signal with event post and wait, and use atomic subroutines."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Teams, events and atomics
**Goal:** advanced image coordination.
```fortran
use, intrinsic :: iso_fortran_env, only: team_type, event_type
type(team_type) :: t
integer :: colour
colour = merge(1, 2, this_image() <= num_images()/2)
form team (colour, t)
change team (t)
  call co_sum(x)
end team
```
- Events: `event post (ev[k])`, `event wait (ev)`, `event_query`.
- Atomics: `atomic_define`, `atomic_ref`, `atomic_add` on `atomic_int_kind` coarrays.
- Support for teams in gfortran/OpenCoarrays has been partial (unconfirmed per version); Intel ifx and NAG implement more.
## Gotchas
- Inside `change team`, `this_image()` is relative to the new team.
- Check the compiler status page before architecting around teams.
## Self-check
Split 4 images into 2 teams and confirm each team's sum separately.
