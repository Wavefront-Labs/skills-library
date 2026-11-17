---
id: computing-software.software-engineering.fortran.do-concurrent-locality
name: do-concurrent-locality
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, do-concurrent-locality, fortran-do-concurrent]
level: advanced
status: draft
description: "Use locality specifiers on do concurrent to declare per-iteration variables and shared data."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Locality specifiers local, local_init, shared, reduce
**Goal:** avoid data races in do concurrent bodies.
```fortran
do concurrent (i = 1:n) local(tmp) shared(a, b)
  tmp = a(i) * 2.0
  b(i) = tmp + 1.0
end do
```
- `local(x)`: each iteration has its own undefined copy. `local_init(x)`: copy initialised from the outer value. `shared(x)`: one shared copy. `default(none)` forces every variable to be named.
- `reduce(+: s)` (Fortran 2023) performs a reduction; confirm your compiler supports it before use (unconfirmed).
## Gotchas
- A scalar temporary not marked `local` is shared, causing a data race if each iteration writes it.
- `forall` is obsolescent in favour of `do concurrent`.
## Self-check
Remove `local(tmp)` and compare against the serial result to observe the race hazard.
