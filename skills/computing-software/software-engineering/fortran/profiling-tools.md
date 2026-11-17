---
id: computing-software.software-engineering.fortran.profiling-tools
name: profiling-tools
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, profiling-tools, fortran-performance]
level: practitioner
status: draft
description: "Profile with gfortran -pg and gprof, Linux perf, and in-code timing with system_clock."
sources:
  - https://gcc.gnu.org/onlinedocs/gfortran/
  - https://gcc.gnu.org/onlinedocs/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Profiling with gprof, perf and timers
**Goal:** find hot spots.
```bash
gfortran -O2 -g -pg -o app *.f90 && ./app && gprof ./app gmon.out | head
perf record -g ./app && perf report        # Linux perf
```
```fortran
integer(int64) :: t0, t1, rate
call system_clock(t0, rate)
! work
call system_clock(t1)
print *, real(t1 - t0, dp) / real(rate, dp), 's'
```
- `cpu_time(t)` measures processor time (not wall-clock); with OpenMP use `omp_get_wtime()`.
- Profile optimised builds with `-g`.
## Gotchas
- `-pg` overhead and inlining distort small functions; use `-fno-inline` for attribution.
- `system_clock` count_rate and wrap-around depend on the integer kind passed.
## Self-check
Time a known loop at two sizes and verify scaling.
