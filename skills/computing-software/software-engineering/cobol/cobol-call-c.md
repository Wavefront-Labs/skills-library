---
id: computing-software.software-engineering.cobol.cobol-call-c
name: cobol-call-c
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, cobol-call-c, cobol-interop, cobol-c-interop, by-value-call, cob-init, entry-point]
level: advanced
status: docs-checked
description: "Pass data between COBOL and C: BY VALUE, BY REFERENCE, data types and GnuCOBOL's cob API."
sources:
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calling C and being called from C (GnuCOBOL)
**Goal:** safe two-way calls.
```cobol
CALL 'c_func' USING BY VALUE WS-INT BY REFERENCE WS-BUF
              RETURNING WS-RC
```
```c
int c_func(int n, char *buf) { return n + (int)strlen(buf); }
```
- `cobc -x main.cob helper.c` links C source directly; `cobc -c helper.c` compiles it only.
- `BY VALUE` passes the numeric value (only numeric literals or items); the default size is 4 bytes, `SIZE AUTO` or `SIZE integer` changes it. `BY REFERENCE` passes an address; `BY CONTENT` passes the address of a copy.
- `RETURNING` takes a numeric item that receives the subroutine's return value.
- Binary items are big-endian by default; set the config option `binary-byteorder` to `native` for native byte order, or use `COMP-5` (native binary integer) for fields shared with C.
- From C: include `libcob.h`, call `cob_init(argc, argv)` first, then either call a statically linked program as a plain C function or use `cob_resolve("name")` to get a pointer (NULL if the module is missing; `cob_resolve_error` returns the message). Finish with `cob_tidy()` or `cob_stop_run(status)`.
- `cob-config --cflags` and `--libs` give the compile and link options when you use `cc` directly.

## Gotchas
- Alphanumeric items have no NUL terminator, so pass a length.
- Compare group layouts byte for byte with the C struct.

## Self-check
Call a C function that returns the sum of two ints from COBOL and print the result.

## Checked
2026-11-02. Checked against the GnuCOBOL manual (C interface chapter, Optimize binary) and Programmer's Guide (CALL, PROCEDURE DIVISION USING, USAGE). Removed: all IBM z/OS Language Environment, ILC, pragma linkage and Java statements, the claim that BY VALUE integers map to `long`, and the `BINARY-LONG` size claim beyond what the Guide states.

Method: documentation only; no commands were run.
