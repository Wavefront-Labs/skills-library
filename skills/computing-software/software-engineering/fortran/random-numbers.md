---
id: computing-software.software-engineering.fortran.random-numbers
name: random-numbers
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, random-numbers, fortran-numeric-intrinsics]
level: practitioner
status: docs-checked
description: "Generate reproducible random numbers with random_init (F2018), random_seed and random_number, and know the generator is processor-dependent."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Random number generation
**Goal:** control randomness.
```fortran
real :: r(5)
integer :: n
call random_seed(size=n)
call random_seed(put=[(i, i=1, n)])      ! fixed seed
call random_number(r)                    ! uniform, 0 <= x < 1
```
- `random_seed([size, put, get])` restarts or queries the generator state used by `random_number`. `size` gives the minimum size of the arrays used with `put` and `get`; they are rank-one default integer arrays.
- Called without arguments, `random_seed` seeds with random data retrieved from the operating system.
- `random_number` for a real argument returns values with 0 <= x < 1. The gfortran runtime implements the xoshiro256** generator.
- As an extension, gfortran `random_number` supports multiple threads; each thread has its own seed, copied from a master seed that `random_seed` (no arguments, or `put`) sets.
- `random_init(repeatable, image_distinct)` (Fortran 2018) initialises the generator; with `repeatable` true the seed is a processor-dependent value that is the same each time it is called from the same image.
## Gotchas
- The algorithm is processor-dependent, so the same seed can give different sequences on different compilers.
## Self-check
Run twice with the same `put` seed and confirm identical sequences.

## Checked
2026-11-02. Confirmed in intrinsic.texi: RANDOM_SEED, RANDOM_NUMBER (range, xoshiro256**, threads), RANDOM_INIT. Removed: 'gfortran 7+ seeds randomly', cryptography/statistical-grade advice, 'processor-dependent across compilers' kept as standard wording only in the gotcha.
Method: documentation only; no commands were run.
