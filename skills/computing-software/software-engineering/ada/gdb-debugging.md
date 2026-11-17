---
id: computing-software.software-engineering.ada.gdb-debugging
name: gdb-debugging
category: computing-software
field: software-engineering
product: ada
tags: [ada, gdb-debugging, gnat-debug-bind]
level: practitioner
status: docs-checked
description: "Debug GNAT programs: -g, gdb break on exception, print Ada values, 'catch exception', backtrace."
sources:
  - https://docs.adacore.com/gnat_ugn-docs/html/gnat_ugn/gnat_ugn/gnat_and_program_execution.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging Ada with GDB
```
gnatmake -g -O0 main        # or gprbuild with -g in the compiler switches
gdb ./main
(gdb) catch exception            # stop when any exception is raised
(gdb) catch exception unhandled  # stop on an exception with no handler
(gdb) break pkg.proc
(gdb) print arr(3)
(gdb) bt
(gdb) info tasks
```
- Debug information comes from `-g`; the guide says it is a GCC/GNAT goal that `-g` does not change the generated code.
- GDB supports a large subset of Ada expression syntax: `print` accepts variables, function calls, operators and attribute references. It acts as if implicit `with` and `use` clauses were in effect for user packages, so names rarely need full qualification.
- `catch exception name` stops on one named exception; `info exceptions` lists the defined Ada exceptions.
- `info tasks` lists the Ada tasks, with the running task marked by an asterisk.
- `up`, `down` and `frame n` move between stack frames after a breakpoint.

## Gotchas
- The guide recommends `-O0` early in development when debugging is needed most, moving to `-O1` and `-O2` later; optimised code makes variable values look odd.

## Self-check
Catch a Constraint_Error in gdb and show the backtrace.

## Checked
Method: docs-checked 2026-11-09 against the GNAT User's Guide page GNAT and Program Execution (debugging with GDB sections, exception catchpoints, tasks, optimisation notes). Dropped `catch assert` and `ptype` examples, which that page does not document.
