---
id: computing-software.software-engineering.cobol.cancel-initial-state
name: cancel-initial-state
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, cancel-initial-state, cancel-statement, initial-program, subprogram-state]
level: intro
status: docs-checked
description: "Reset a subprogram's state with CANCEL or the INITIAL attribute, and know what each does to files and WORKING-STORAGE."
sources:
  - https://www.ibm.com/docs/en/cobol-zos/6.4?topic=statements-cancel-statement
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CANCEL, INITIAL and subprogram state
**Goal:** predictable state between calls (Enterprise COBOL for z/OS rules).

- A program is in its initial state the first time it is called in a run unit, and after a CANCEL naming it (or a program that contains it). In the initial state WORKING-STORAGE items with a VALUE clause take that value (items without VALUE are undefined) and files with internal file connectors are not open. Later calls otherwise reuse the last values.
- `CANCEL 'SUBPGM'` (literal or identifier holding the program name) makes the next CALL enter the subprogram in its initial state. The name must match the one used in an associated CALL. Programs contained in the cancelled program are also cancelled.
- `PROGRAM-ID. X IS INITIAL.` puts the program (and programs nested in it) in the initial state on every call. IS INITIAL is not supported with the THREAD compiler option.
- CANCEL closes open files that have an internal file connector in the named program; USE procedures for them are not executed. Do not rely on this: CLOSE explicitly.
- A subprogram must not CANCEL its caller or any program above it in the calling hierarchy; the run unit is terminated.

## Gotchas
- CANCEL does nothing if the program was never dynamically called in this run unit or was already cancelled.
- Contents of EXTERNAL data records described by the cancelled program are not changed by CANCEL.
- In a multithreaded environment a program that is active on any thread cannot be cancelled.
- The program named in CANCEL must have been called and have returned via EXIT PROGRAM or GOBACK.

## Self-check
Call twice, CANCEL, call again: counters read 1, 2, 1.

## Checked
Date: 2026-11-08. Read the whole IBM docs CANCEL statement page and, in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted), the PROGRAM-ID paragraph INITIAL clause text. Confirmed every bullet above. Trimmed: "closes them in some runtimes" (replaced with IBM's rule), the claim that CANCEL breaks saved pointers (not documented), and the claim about statically bound programs (replaced with the documented no-action condition). Removed the unread ISO and GnuCOBOL sources and the LOCAL-STORAGE mention in the description (the body never covered it).
Method: documentation only; no commands were run.
