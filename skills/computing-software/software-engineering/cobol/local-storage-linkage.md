---
id: computing-software.software-engineering.cobol.local-storage-linkage
name: local-storage-linkage
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, local-storage-linkage, cobol-storage-sections, local-storage-section, linkage-section]
level: practitioner
status: docs-checked
description: "Use LOCAL-STORAGE for per-invocation data and LINKAGE for parameters and addressed storage in Enterprise COBOL."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LOCAL-STORAGE and LINKAGE SECTION
**Goal:** know which section gives per-call or externally owned data (Enterprise COBOL for z/OS 6.4).

- `LOCAL-STORAGE SECTION`: storage is allocated and freed per invocation; on each invocation items are reallocated and every item with a VALUE clause is initialized to it. Allowed in recursive and non-recursive programs, methods and user-defined functions. Items cannot carry EXTERNAL. For nested programs the storage is allocated on each invocation of the outermost program, but items are re-initialized each time the nested program is invoked.
- `LINKAGE SECTION`: entries give names and descriptions, but no storage is reserved because the data area exists elsewhere (the caller's parameters, or storage whose address you set). Any data description clause except EXTERNAL may be used.
- A recursive program's WORKING-STORAGE is static and shared across invocations; its LOCAL-STORAGE is per-invocation.
- The `ADDRESS OF` special register of a 01 or 77 LINKAGE item can be both sent and received (use `SET ADDRESS OF item TO pointer`); for other items it is send-only. It is implicitly USAGE POINTER, and NULL has the value zero.
```cobol
LINKAGE SECTION.
01 LS-PARM-IN.
   05 LS-PARM-LEN PIC S9(4) COMP.
   05 LS-PARM-TXT PIC X(100).
PROCEDURE DIVISION USING LS-PARM-IN.
```

## Gotchas
- ADDRESS OF can be compared with NULL (the manual's table of permissible pointer comparisons), so `IF ADDRESS OF item = NULL` is a valid way to test whether a LINKAGE item has been given an address.
- LOCAL-STORAGE VALUE clauses are re-applied on every call; WORKING-STORAGE ones only in the program's initial state.

## Self-check
Write a recursive factorial with its work fields in LOCAL-STORAGE and the program marked RECURSIVE; the result for 5 is 120.

## Checked
2026-11-08. Confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference (Chapter 24 LOCAL-STORAGE SECTION, LINKAGE SECTION; Chapter 15 RECURSIVE and INITIAL; special registers ADDRESS OF and NULL). Removed: "needed for RECURSIVE programs and threaded code", the allocation-cost claim, the OMITTED and addressing-abend claims, the PARM halfword-length claim (Programming Guide not read), and the ISO and GnuCOBOL sources.
Method: documentation only; no commands were run.
