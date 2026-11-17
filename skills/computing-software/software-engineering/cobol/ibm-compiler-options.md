---
id: computing-software.software-engineering.cobol.ibm-compiler-options
name: ibm-compiler-options
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, ibm-compiler-options, cobol-compiler-ibm, compiler-options, ssrange, arith-compat, opt-level]
level: advanced
status: draft
description: "Pick compile-time options for correctness, debugging and performance on Enterprise COBOL for z/OS."
sources:
  - https://www.ibm.com/docs/en/cobol-zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enterprise COBOL compiler options (ARITH, TRUNC, SSRANGE, OPT, RENT, LIST, XREF)
**Goal:** a known-good options baseline per environment.

Common options (PARM on the compile step or `CBL`/`PROCESS` statements at the top of the source):
- `ARITH(EXTEND)` 31-digit arithmetic; `ARITH(COMPAT)` 18 digits.
- `TRUNC(STD|OPT|BIN)` binary field truncation behavior (see decimal-precision skill).
- `SSRANGE` runtime subscript and reference-mod checking (development; costs time).
- `OPT(0|1|2)` optimization; use OPT(0) with debuggers; higher levels for production.
- `RENT` reentrant code (required for CICS and for dynamic subprograms in many shops).
- `LIST`, `MAP`, `XREF`, `OFFSET` produce listings used in dump analysis (OFFSET gives statement offsets for abend analysis).
- `NUMPROC(PFD|NOPFD|MIG)` sign handling; `DYNAM|NODYNAM`; `LIB` for COPY processing; `CODEPAGE(ccsid)`.
```cobol
CBL ARITH(EXTEND),TRUNC(STD),SSRANGE,OFFSET,XREF
 IDENTIFICATION DIVISION.
```
- Set installation-wide defaults with the installation options module; individual jobs override unless the option is locked (NOOPTIONS rules per site).

## Gotchas
- Option names and defaults change between compiler versions (V4 vs V6); verify with the Programmer's Guide of your release.
- A program compiled with different TRUNC than its callers can still interoperate, but results may differ at boundaries.

## Self-check
Compile with the listing and read the "options in effect" section to confirm the baseline.
