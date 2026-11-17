---
id: computing-software.software-engineering.fortran.select-case
name: select-case
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, select-case, fortran-control-flow]
level: intro
status: draft
description: "Branch on integer, logical or character values with select case, case ranges and case default."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# select case construct
**Goal:** replace if chains with select case.
```fortran
select case (code)
case (1)
  print *, 'one'
case (2:4, 10)
  print *, 'two to four or ten'
case default
  print *, 'other'
end select
```
- Selector types: integer, logical, character (not real).
- Ranges: `case (:0)` for up to 0, `case (100:)` for 100 and above.
- No fallthrough: only one case runs.
- Character cases compare as if blank-padded.
## Gotchas
- Overlapping case values are a compile error.
- For real or complicated conditions use `if`/`else if`.
## Self-check
Pass 3 and confirm the range case runs.
