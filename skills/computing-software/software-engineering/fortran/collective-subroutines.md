---
id: computing-software.software-engineering.fortran.collective-subroutines
name: collective-subroutines
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, collective-subroutines, fortran-coarrays]
level: advanced
status: docs-checked
description: "Reduce and broadcast across images with co_sum, co_max, co_min, co_broadcast and co_reduce."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collective subroutines
**Goal:** use the collective intrinsics.
- `CO_SUM(A [, RESULT_IMAGE, STAT, ERRMSG])` sums each element of `A` over all images of the current team; with `RESULT_IMAGE` the result is returned only on that image and `A` is undefined on the others; without it the result is on all images.
- `CO_MAX(A [, RESULT_IMAGE, STAT, ERRMSG])` is the element-wise maximum (integer, real or character `A`), with the same `RESULT_IMAGE` rule.
- `CO_BROADCAST(A, SOURCE_IMAGE [, STAT, ERRMSG])` copies `A` from `SOURCE_IMAGE` to all images of the current team.
- `CO_REDUCE(A, OPERATION [, RESULT_IMAGE, STAT, ERRMSG])` reduces element-wise with a pure two-argument function `OPERATION`.
- On success `STAT` is set to zero; on failure it is nonzero and `ERRMSG` describes the error.
- `A` must have the same type and type parameters on all images (and the same shape if an array).
```fortran
real :: x
x = real(this_image())
call co_sum(x)
```
- The manual lists these under Technical Specification 18508 or later.
## Gotchas
- They need a coarray runtime: see `-fcoarray=`.
## Self-check
Sum `this_image()` over 4 images and compare with 4*5/2.

## Checked
2026-11-02. Confirmed in intrinsic.texi: CO_SUM, CO_MAX, CO_BROADCAST, CO_REDUCE arguments and semantics, STAT/ERRMSG, same-type rule, TS 18508 note. Removed: 'hang on subset of images', OpenCoarrays support claim, 'arguments need not be coarrays' (not stated).
Method: documentation only; no commands were run.
