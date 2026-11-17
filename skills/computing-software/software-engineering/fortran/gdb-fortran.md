---
id: computing-software.software-engineering.fortran.gdb-fortran
name: gdb-fortran
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, gdb-fortran, fortran-debugging]
level: practitioner
status: draft
description: "Debug gfortran programs in gdb: break on lines and run-time errors, print arrays and derived types, and use the Fortran language mode."
sources:
  - https://gcc.gnu.org/onlinedocs/gfortran/
  - https://sourceware.org/gdb/documentation/
  - https://valgrind.org/docs/manual/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debugging Fortran with gdb
**Goal:** step through code.
```bash
gfortran -g -O0 -o app main.f90
gdb ./app
(gdb) break main.f90:42
(gdb) run
(gdb) print a              # whole array
(gdb) print a(2:4)         # slice
(gdb) ptype p              # derived type layout
(gdb) info locals
(gdb) backtrace
```
- Break on runtime errors: `break _gfortran_runtime_error` and `break _gfortran_os_error` (library function names; verify with `info functions _gfortran_` in your install).
- Print allocatable arrays by name after allocation; gdb understands Fortran descriptors for gfortran.
- Set `set language fortran` if gdb picks C.
## Gotchas
- Optimised code hides variables; use `-O0` or `-Og`.
- Module variables are named `__module_MOD_name` in symbols.
## Self-check
Break at a line, print an array section, and step with `next`.
