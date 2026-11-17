---
id: computing-software.software-engineering.cobol.working-storage
name: working-storage
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, working-storage, cobol-storage-sections, working-storage-section, static-storage]
level: intro
status: docs-checked
description: "Use WORKING-STORAGE for program data, VALUE initial values, and know when it persists or resets (INITIAL, CANCEL, LOCAL-STORAGE)."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WORKING-STORAGE SECTION and initial values
**Goal:** declare program state correctly (Enterprise COBOL for z/OS 6.4).

```cobol
WORKING-STORAGE SECTION.
01 WS-SWITCHES.
   05 WS-EOF-SW   PIC X VALUE 'N'.
      88 AT-EOF   VALUE 'Y'.
01 WS-LIMIT       PIC 9(3) VALUE 100.
```
- The section starts with the header `WORKING-STORAGE SECTION.` and holds records not part of files and independent items (level 77 or 01).
- A program's WORKING-STORAGE is initialized the first time it is called in a run unit, and again after a CANCEL of the program (or of a program containing it). If the program has the `INITIAL` attribute (`PROGRAM-ID. X IS INITIAL`) it is initialized on every call. Between other calls it keeps its last-used values.
- In the initial state, an item with a VALUE clause gets that value; an item without one has an undefined initial value.
- A VALUE on a group initializes the whole group area without regard to its subordinate entries, and subordinate entries then must not have VALUE. A VALUE on an item with OCCURS applies to every occurrence.
- Use the INITIALIZE statement to reset data during processing; VALUE applies only when the program enters its initial state.
- By default WORKING-STORAGE is above the 2 GB bar under LP(64) and below it under LP(32); the DATA compiler option controls the 24/31-bit location.
- Use LOCAL-STORAGE instead when data must be reallocated and VALUE-initialized on every invocation (see local-storage-linkage).

## Gotchas
- Re-calling a non-INITIAL subprogram starts with the previous call's values, not the VALUE clauses.
- Never rely on an item without VALUE having any particular content.
- VALUE must not be used on an item that is, or is subordinate to, an item with REDEFINES or EXTERNAL.

## Self-check
Call the program twice in one run unit: counters carry over unless the program is INITIAL or was CANCELled in between.

## Checked
2026-11-08. Confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference (Chapter 24 WORKING-STORAGE SECTION; Chapter 15 PROGRAM-ID INITIAL and RECURSIVE; Chapter 26 VALUE clause). Removed: the claim that CONSTANT entries are accepted by some compilers including IBM or GnuCOBOL (the 6.4 manual documents no CONSTANT data entry), "group VALUE initializes at load time only" (reworded to the manual's initial-state rule), "zeros in some compilers" and the ISO source.
Method: documentation only; no commands were run.
