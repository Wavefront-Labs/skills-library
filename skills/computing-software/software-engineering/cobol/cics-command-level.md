---
id: computing-software.software-engineering.cobol.cics-command-level
name: cics-command-level
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, cics-command-level, cobol-cics, exec-cics, cics-translator, dfhcommarea, eib]
level: advanced
status: draft
description: "Structure a command-level CICS COBOL program: EXEC CICS blocks, EIB, DFHCOMMAREA and the translate step."
sources:
  - https://www.ibm.com/docs/en/cics-ts
  - https://www.ibm.com/docs/en/cobol-zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EXEC CICS command-level COBOL programs and the translator
**Goal:** the skeleton of a CICS COBOL transaction.

```cobol
WORKING-STORAGE SECTION.
01 WS-COMM PIC X(100).
LINKAGE SECTION.
01 DFHCOMMAREA PIC X(100).
PROCEDURE DIVISION.
    EXEC CICS RETURN END-EXEC.
```
- CICS commands are `EXEC CICS ... END-EXEC`; a translator (or integrated coprocessor) converts them to CALLs before/during compilation.
- The translator inserts the EIB (EXEC Interface Block, `EIBCALEN`, `EIBTRNID`, `EIBAID`, `EIBRESP` etc.) as the first LINKAGE item and the COMMAREA is `DFHCOMMAREA`.
- Programs must be compiled with RENT in many shops and defined as PROGRAM/TRANSACTION resources in CICS.
- Never use DISPLAY, ACCEPT, STOP RUN, or native COBOL file I/O in CICS programs; use EXEC CICS equivalents and `RETURN`.

## Gotchas
- Missing or too-short DFHCOMMAREA is detected with `EIBCALEN = 0` on first entry.
- Large working storage is allocated per task; keep it modest.

## Self-check
Run the transaction; first entry has EIBCALEN = 0, and re-entry passes the COMMAREA.
