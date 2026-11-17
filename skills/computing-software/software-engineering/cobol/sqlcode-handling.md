---
id: computing-software.software-engineering.cobol.sqlcode-handling
name: sqlcode-handling
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, sqlcode-handling, cobol-db2, sqlcode-checking, null-indicator, varchar-host-variable, sqlstate]
level: advanced
status: draft
description: "Interpret SQLCODE/SQLSTATE and handle NULLs and VARCHAR columns correctly in COBOL."
sources:
  - https://www.ibm.com/docs/en/db2-for-zos
  - https://www.ibm.com/docs/en/cobol-zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SQLCODE, SQLSTATE, null indicators and VARCHAR host variables
**Goal:** error and NULL handling that does not corrupt data.

```cobol
01 WS-NAME.
   49 WS-NAME-LEN  PIC S9(4) COMP.
   49 WS-NAME-TEXT PIC X(30).
01 WS-BAL-IND PIC S9(4) COMP.
...
IF WS-BAL-IND < 0 MOVE ZERO TO WS-BAL END-IF.
EXEC SQL GET DIAGNOSTICS CONDITION 1 :WS-MSG = MESSAGE_TEXT END-EXEC.
```
- Common SQLCODEs: 0 success, +100 no row, -803 duplicate key, -811 multiple rows in SELECT INTO, -904 resource unavailable, -911/-913 deadlock/timeout (retry), -305 NULL returned without an indicator.
- SQLSTATE is the portable code (e.g. 23505 unique violation, 40001 deadlock).
- Indicator variable: negative means NULL; set -1 before INSERT/UPDATE to store NULL.
- VARCHAR columns map to a group with 49-level length and text fields.
- `DSNTIAR` formats SQLCA messages (z/OS callable utility; arguments per DB2 docs, verify).

## Gotchas
- Retry logic on -911/-913 must roll back and restart the unit of work.
- Date and timestamp columns can map to PIC X(10) / X(26).

## Self-check
Insert a duplicate key and confirm -803 is mapped to a friendly message.
