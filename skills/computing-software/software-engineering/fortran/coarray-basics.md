---
id: computing-software.software-engineering.fortran.coarray-basics
name: coarray-basics
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, coarray-basics, fortran-coarrays]
level: advanced
status: docs-checked
description: "Choose gfortran -fcoarray modes and use this_image and num_images."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coarray declaration and images
**Goal:** write SPMD Fortran.
- `-fcoarray=<keyword>`: `none` (default; coarray use is a compile error), `single` (single-image mode, `num_images()` is always 1), `shared` (shared-memory multithreading), `lib` (a library such as OpenCoarrays, or GCC's `libcaf_single` for one image, must be linked).
```bash
gfortran -fcoarray=single -o app main.f90
```
- `this_image()` returns the image index (Fortran 2008) and `num_images()` the number of images in the current team.
- Collective procedures such as `co_sum`, `co_max`, `co_reduce` and `co_broadcast` are covered by the collective-subroutines skill.
## Gotchas
- Syntax and rules for declaring and accessing coarrays (`[*]` codimensions, `sync all`, `save` requirement) are defined by the Fortran standard, not by the gfortran manual pages checked here; confirm them in the standard.
## Self-check
Compile with `-fcoarray=single` and confirm `num_images()` returns 1.

## Checked
2026-11-02. Confirmed in invoke.texi (-fcoarray values and meanings) and intrinsic.texi (THIS_IMAGE, NUM_IMAGES). Removed: the program example, cafrun/caf wrapper commands, codimension syntax and sync/save rules (standard-text claims not on pages read).
Method: documentation only; no commands were run.
