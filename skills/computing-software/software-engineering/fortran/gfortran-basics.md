---
id: computing-software.software-engineering.fortran.gfortran-basics
name: gfortran-basics
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, gfortran-basics, fortran-gfortran]
level: intro
status: docs-checked
description: "Compile single files and multi-file programs with gfortran, choose output names, compile only with -c, and select source form and standard."
sources:
  - https://gcc.gnu.org/onlinedocs/gfortran/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compiling and linking with gfortran
**Goal:** build programs from the command line.
```bash
gfortran -o app main.f90                      # compile + link
gfortran -c geometry.f90                      # object file; a module also produces a .mod file
gfortran -J build/mod -c geometry.f90         # -J: where .mod files are written (also searched by USE)
gfortran -I build/mod -c main.f90             # -I: extra search directory
gfortran -std=f2018 -o app main.f90
gfortran --version
```
- `-J<dir>` sets where `.mod` files are put (default: current directory) and adds `<dir>` to the directories searched by `USE`.
- `-std=` accepts `f95`, `f2003`, `f2008`, `f2018` (and `f2023`, `gnu`, `legacy`); see the Fortran dialect options.
- Link libraries with the GCC driver options `-L<dir>` and `-l<name>`.
- `-cpp` enables preprocessing; it runs automatically for `.fpp`, `.FPP`, `.F`, `.FOR`, `.FTN`, `.F90`, `.F95`, `.F03`, `.F08`.
- `-ffree-form` / `-ffixed-form` set the source layout; with neither, the file extension decides.
## Gotchas
- A module's `.mod` file must exist before a file that `USE`s it is compiled, so compile the module source first.
## Self-check
Compile a module file and a main program that uses it, in that order, and run the result.

## Checked
2026-11-02. Confirmed in the GNU Fortran manual (invoke): -J and -I semantics, -std values, -cpp extension list, -ffree-form/-ffixed-form default rule; -L/-l are GCC driver options. Removed: version-mixing .mod claim and command-line ordering claim (not stated in the manual pages read).
Method: documentation only; no commands were run.
