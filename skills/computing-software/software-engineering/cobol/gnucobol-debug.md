---
id: computing-software.software-engineering.cobol.gnucobol-debug
name: gnucobol-debug
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, gnucobol-debug, cobol-debugging, cobc-debug-flags, cob-set-trace, gdb-cobol, debugging-mode]
level: practitioner
status: docs-checked
description: "Find bugs in GnuCOBOL programs with runtime checks, tracing, DISPLAY debugging and gdb."
sources:
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging GnuCOBOL with --debug, tracing and the system debugger
**Goal:** the shortest path to the failing line.
```bash
cobc -x --debug -g -Wall prog.cob
cobc -x -ftraceall prog.cob
COB_SET_TRACE=Y COB_TRACE_FILE=trace.log ./prog
```
- `--debug` (`-d`) enables all run-time error checking (equal to `-fstack-check -fec=EC-ALL`) such as subscript bounds and numeric data checks, and shows run-time errors with source locations.
- `-ftrace` generates trace code for executed SECTION/PARAGRAPH; `-ftraceall` also traces STATEMENTs. Set `COB_SET_TRACE` to switch tracing on at run time; `COB_TRACE_FILE` redirects it (default stderr). `--debug` does not imply `-ftrace`, so add the flag explicitly.
- `-fdebugging-line` enables debugging lines (`D` in the indicator column, or floating `>>D`).
- `-g` adds C compiler debug information and stack checking so you can step through the COBOL code and inspect the call stack with the system debugger; the manual says direct access to COBOL variables needs a GDB frontend that provides it.
- `COB_CORE_ON_ERROR` and `COB_CORE_FILENAME` control core dumps and `-fdump` memory dumps are available per module; `--save-temps` keeps the generated C.

## Gotchas
- Runtime checks change performance; do not ship `--debug` builds unless intended.
- Tracing every statement of a long batch run produces huge logs; use a small input.

## Self-check
Index a table one past its end in a `--debug` build and see the run-time error with its source location.

## Checked
2026-11-02. Checked against the GnuCOBOL manual (Debug chapter, compile options) and Programmer's Guide (cobc option list, COB_SET_TRACE, COB_SET_DEBUG), the NEWS note that -debug no longer implies -ftrace, and flag.def help text. Corrected: the old text wrote `-debug`, the documented option is `--debug`/`-d`. Removed: the specific list of what file state checks cover and the claim about mapping gdb output to generated C beyond what the manual states.

Method: documentation only; no commands were run.
