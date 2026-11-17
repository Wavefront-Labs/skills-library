---
id: computing-software.software-engineering.cobol.dynamic-vs-static-call
name: dynamic-vs-static-call
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, dynamic-vs-static-call, cobol-subprograms, static-call, dynamic-call, call-by-name, call-literal]
level: advanced
status: docs-checked
description: "Know the difference between CALL literal and CALL identifier, what the linker or loader does, and how to pick one."
sources:
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static and dynamic CALL (GnuCOBOL)
**Goal:** control binding time.
- `CALL "subr"` (literal) is resolved at run time by default; compiling with `-fstatic-call` links the called program at compile time. The option only affects a literal name: `CALL SUBR` (identifier) is always dynamic.
- Per call, `CALL STATIC "subr"` forces static linkage for just that subroutine.
- Dynamic: the module is built with `cobc -m`, found via `COB_LIBRARY_PATH` (or the current directory) and its file name (minus the OS extension) must match the primary entry-point name.
- `COB_PRE_LOAD` pre-loads modules at program start; it only reaches modules called by literal.
- Static linking checks that every called program is present in the resulting binary and is slightly faster.
```bash
cobc -x -o prog main.cob subr1.cob subr2.cob   # one executable
cobc -m subr.cob                                # subr.so, loaded at CALL time
```
- `ON EXCEPTION` (same as `ON OVERFLOW`) runs when the subroutine cannot be located or loaded at run time; `NOT ON EXCEPTION` runs on success.
- A dynamically loaded module is unloaded on `CANCEL` only when `COB_PHYSICAL_CANCEL` is set.

## Gotchas
- Calls to a module that is missing fail at run time, not at compile time, unless it is linked statically.

## Self-check
Rename the module on disk and confirm `ON EXCEPTION` runs rather than a crash.

## Checked
2026-11-02. Checked against the GnuCOBOL manual (Optimize call, Static linking, Dynamic linking) and the Programmer's Guide CALL statement and runtime-configuration entries (COB_PRE_LOAD, COB_PHYSICAL_CANCEL). Removed: all IBM statements (NODYNAM/DYNAM options, STEPLIB/LIBDEF, abend S806), the unsupported claim that name case and length rules differ between systems, and the claim that CANCEL always unloads.

Method: documentation only; no commands were run.
