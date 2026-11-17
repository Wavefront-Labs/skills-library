---
id: computing-software.software-engineering.d.d-dmd-common-switches
name: d-dmd-common-switches
category: computing-software
field: software-engineering
product: d
tags: [d-dmd-common-switches, dmd-compiler, dmd, dmd-switches, -of, -od, -i, -release, -inline, -g, -w, compiler-flags, d]
level: intro
status: docs-checked
description: "Drive dmd from the command line: output names (-of, -od), -c compile only, -i auto-import, optimisation -O -inline -release, debug -g, warnings -w -wi, and linker -L."
sources:
  - https://dlang.org/dmd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dmd command line: -of -od -c -i -O -release -inline -g -w -wi -I -L

Goal: compile and tune builds with dmd.

- Basic: `dmd app.d util.d -ofapp` builds an executable; `dmd -c a.d` makes `a.o`/`a.obj`; `-lib` makes a library instead of object files; `-shared`; `-fPIC` generates position independent code (not on Windows or macOS).
- Layout: `-od<dir>` object dir, `-of<file>` output file, `-I<dir>` import path, `-J<dir>` string-import path, `-L<flag>` pass to linker (`-L-lm`), `-i` includes imported modules in the compilation.
- Quality: `-w` warnings as errors, `-wi` warnings as messages, `-de` deprecations are errors, `-dw` deprecation messages (default), `-unittest`, `-main`, `-debug`, `-version=X`, `-preview=<x>`, `-revert=<x>`, `-transition=<x>`, `-vcolumns`, `-verrors=N`, `-checkaction=context`, `-betterC`, `-cov`.
- Speed: `-O -release -inline -boundscheck=off` (`-release` keeps bounds checks in `@safe` functions unless `-boundscheck=off`), `-mcpu=baseline|avx|native`, `-m64`/`-m32`, `-profile`, `-profile=gc`.
- Debug: `-g` symbolic debug info (CodeView on Windows), `-gf` debug info for all referenced types, `-gs` always emit a stack frame.
- Info: `dmd --version`, `-v` verbose output for each compiler pass, `-vgc` lists GC allocations, `-vtls` lists thread-local variables, `-H` generates a D interface file, `-D` documentation, `-X` JSON file.

Gotchas:
- On Windows `-m64` object code is MS-COFF; `-m32mscoff` is the 32-bit MS-COFF switch.

Verify: `dmd -v hello.d` prints verbose output for each compiler pass.

## Checked

Date 2026-11-02. Confirmed switch meanings against the DMD command line page. Errors fixed: -m32omf is not a listed switch (-m32mscoff is); -defaultlib=libphobos2.so removed; -mcpu values are baseline|avx|native; -dw, -w and -wi descriptions corrected.

Method: documentation only; no commands were run.
