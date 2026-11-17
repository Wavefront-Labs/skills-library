---
id: computing-software.software-engineering.fortran.sync-images
name: sync-images
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, sync-images, fortran-coarrays]
level: advanced
status: draft
description: "Order access across images with sync all, sync images, sync memory, critical and lock."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Synchronisation statements
**Goal:** avoid races between images.
```fortran
if (this_image() == 1) a[2] = 5.0
sync all                                  ! barrier
if (this_image() == 2) print *, a
sync images ([1, 2])                      ! pairwise sync
critical
  counter[1] = counter[1] + 1
end critical
```
- `sync all`: barrier across all images. `sync images(list)`: only listed images. `sync memory`: memory fence.
- `lock_type` with `lock`/`unlock` for mutual exclusion.
- Segment ordering is defined only by these statements.
## Gotchas
- Each `sync images` pair must be matched on both sides or the program deadlocks.
- `stop` on one image does not stop others unless `error stop`.
## Self-check
Remove the `sync all` and observe the data race on a multi-image run.
