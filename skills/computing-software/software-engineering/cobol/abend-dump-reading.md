---
id: computing-software.software-engineering.cobol.abend-dump-reading
name: abend-dump-reading
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, abend-dump-reading, cobol-debugging, s0c7, s0c4, s806, s322, abend-codes]
level: advanced
status: draft
description: "Diagnose common z/OS COBOL abends from codes, CEEDUMP and the compile listing."
sources:
  - https://www.ibm.com/docs/en/cobol-zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading abends and dumps (S0C7, S0C4, S0CB, S806, S322)
**Goal:** go from abend code to source line fast.

| Abend | Typical cause |
|---|---|
| S0C7 | data exception: invalid packed/zoned data in arithmetic |
| S0C4 | protection exception: bad subscript, unset pointer, LINKAGE item not passed |
| S0CB | divide by zero (no SIZE ERROR) |
| S806 | module not found (dynamic CALL or EXEC PGM) |
| S322 | CPU time limit exceeded (often an infinite loop) |
| S0C1 | operation exception: branch into data, CALL to non-code |
| U4038 | LE abend (condition severity) |
Method:
1. Get the failing offset from the abend message or CEEDUMP traceback.
2. Compile with `LIST`/`OFFSET` (or `TEST`) and find the statement near that offset in the listing.
3. Inspect the fields used there (dump hex): NUMERIC test the suspect field.
4. For S0C7, check READ INTO records, uninitialized working storage and group MOVE onto packed fields.

## Gotchas
- Optimized code (OPT(1/2)) reorders statements; debug builds at OPT(0).
- Some codes (such as 806) have reason codes in the message text that decide the fix.

## Self-check
Create an S0C7 by moving spaces to a packed field then adding to it; trace it back to the line using the listing.
