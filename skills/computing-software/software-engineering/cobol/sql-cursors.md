---
id: computing-software.software-engineering.cobol.sql-cursors
name: sql-cursors
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, sql-cursors, cobol-db2, declare-cursor, fetch-loop, with-hold, for-update-of]
level: advanced
status: draft
description: "Process multi-row result sets with cursors and update through them safely."
sources:
  - https://www.ibm.com/docs/en/db2-for-zos
  - https://www.ibm.com/docs/en/cobol-zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cursors: DECLARE, OPEN, FETCH, CLOSE and WITH HOLD
**Goal:** the standard cursor loop.

```cobol
EXEC SQL DECLARE C1 CURSOR FOR
    SELECT CUST_ID, NAME FROM CUSTOMER
     WHERE REGION = :WS-REGION
     ORDER BY CUST_ID
END-EXEC.
EXEC SQL OPEN C1 END-EXEC.
PERFORM UNTIL SQLCODE NOT = 0
    EXEC SQL FETCH C1 INTO :WS-ID, :WS-NAME END-EXEC
    IF SQLCODE = 0 PERFORM PROCESS-ROW END-IF
END-PERFORM.
EXEC SQL CLOSE C1 END-EXEC.
```
- DECLARE appears before use in the source; OPEN binds host variable values at open time.
- `WITH HOLD` keeps the cursor across COMMIT; `FOR UPDATE OF col` plus `UPDATE ... WHERE CURRENT OF C1` updates the fetched row.
- Row-set (multi-row) FETCH with arrays is available on DB2 for z/OS (`FETCH ... FOR :n ROWS`) for performance.
- COMMIT frequency: commit every n rows in batch jobs and use WITH HOLD plus saved restart keys.

## Gotchas
- After SQLCODE +100, stop fetching; do not process the last host-variable values.
- A cursor left open at program end is closed by DB2 at commit/termination, but close explicitly.

## Self-check
Fetch all rows for a region, count them, and compare with `SELECT COUNT(*)`.
