---
id: computing-software.software-engineering.fortran.namelist-io
name: namelist-io
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, namelist-io, fortran-io-formatted]
level: practitioner
status: draft
description: "Read and write grouped named variables with namelist for configuration files."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Namelist I/O
**Goal:** use namelist for simple configs.
```fortran
integer :: n = 10
real :: dt = 0.01
namelist /params/ n, dt
open (newunit=u, file='input.nml', status='old', action='read')
read (u, nml=params)
close (u)
```
Input file:
```
&params
  n = 20
  dt = 0.005
/
```
- Variables absent in the file keep their current values.
- Arrays, derived types and strings can be in namelists.
- `iostat`/`iomsg` give the error text for unknown names.
## Gotchas
- Group name and variable names are case-insensitive.
- Namelist formatting differs slightly across compilers on output; parse with the same compiler for round trips.
## Self-check
Change `n` in the file and confirm the program prints 20.
