---
id: computing-software.software-engineering.cobol.initialize-vs-move
name: initialize-vs-move
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, initialize-vs-move, initialize-statement, set-statement, move-statement]
level: intro
status: docs-checked
description: "Pick the right reset: INITIALIZE for records, MOVE for simple items, SET for index/condition/pointer values."
sources:
  - https://www.ibm.com/docs/en/cobol-zos/6.4?topic=statements-initialize-statement
  - https://www.ibm.com/docs/en/cobol-zos/6.4?topic=statements-set-statement
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6pg40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing MOVE, INITIALIZE or SET for resetting data
**Goal:** avoid the group-MOVE-spaces trap (Enterprise COBOL for z/OS rules).

| Need | Use |
|---|---|
| Clear a record with numerics | `INITIALIZE rec` |
| Blank a pure text field | `MOVE SPACES TO fld` |
| Zero an accumulator | `MOVE ZERO TO acc` |
| Change an index | `SET ix TO 1`, `SET ix UP BY 1` |
| Set a flag via 88 | `SET cond TO TRUE` |
| Set a pointer | `SET ptr TO ADDRESS OF item` |
- INITIALIZE acts as a series of implicit MOVEs to each elementary item: alphabetic, alphanumeric, alphanumeric-edited, DBCS, national and UTF-8 items get SPACE; numeric and numeric-edited items get ZERO. `REPLACING category BY value` and `WITH FILLER`, `ALL TO VALUE`, `THEN TO DEFAULT` change that.
- Output record layouts mixing text and packed fields should be built with INITIALIZE and then field MOVEs.
- `SET cond TO TRUE` places the condition's first VALUE literal in its conditional variable; `SET cond TO FALSE` requires a WHEN SET TO FALSE phrase on the condition-name.
- `SET ix UP BY n` / `DOWN BY n` adjust an index by n occurrences, and the index must hold a valid occurrence number before and after.

## Gotchas
- `MOVE LOW-VALUES TO rec` on a record with COMP-3 fields creates invalid packed data (LOW-VALUE is X'00' in EBCDIC alphanumeric data): the sign nibble would be X'0', and the compiler accepts only X'A' to X'F'.
- INITIALIZE does not touch FILLER items unless you code the FILLER phrase. It also skips items with REDEFINES or RENAMES, and cannot initialize variable-length (OCCURS DEPENDING ON) or variably-located items.
- The value of an index after SEARCH or PERFORM can be undefined: reinitialize with SET before other table operations.

## Self-check
After clearing a mixed record, write it to a file and confirm a downstream reader can parse each packed field.

## Checked
Date: 2026-11-08. Read the whole IBM docs INITIALIZE and SET pages (the SET page is only an overview), and in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the INITIALIZE statement and rules and SET formats 1 to 5; in the Programming Guide PDF the NUMPROC option text for valid sign nibbles (X'A' to X'F'). Confirmed the default sending values, FILLER and REDEFINES exclusions, ODO restriction, SET condition-name and index rules. Trimmed "on most compilers" to the IBM statement. Removed the unread ISO and GnuCOBOL roots. Also read the Figurative constants section (LOW-VALUE is X'00' for EBCDIC alphanumeric data); the MOVE page does not cover figurative constants, so the table rows rely on the INITIALIZE implied SPACE/ZERO senders.
Method: documentation only; no commands were run.
