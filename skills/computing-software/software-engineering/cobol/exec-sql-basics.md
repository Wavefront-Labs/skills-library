---
id: computing-software.software-engineering.cobol.exec-sql-basics
name: exec-sql-basics
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, exec-sql-basics, cobol-db2, exec-sql, host-variables, sqlca, dclgen]
level: advanced
status: draft
description: "Embed SQL in COBOL with host variables, the SQLCA, DCLGEN structures and SELECT INTO."
sources:
  - https://www.ibm.com/docs/en/db2-for-zos
  - https://www.ibm.com/docs/en/cobol-zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EXEC SQL, host variables, SQLCA and INCLUDE
**Goal:** correct basic embedded SQL.

```cobol
EXEC SQL INCLUDE SQLCA END-EXEC.
EXEC SQL INCLUDE CUSTDCL END-EXEC.        *> DCLGEN output
...
EXEC SQL
    SELECT NAME, BALANCE
      INTO :CUST-NAME, :CUST-BAL:CUST-BAL-IND
      FROM CUSTOMER
     WHERE CUST_ID = :WS-CUST-ID
END-EXEC.
IF SQLCODE = 0 CONTINUE
ELSE IF SQLCODE = +100 PERFORM NOT-FOUND
ELSE PERFORM SQL-ERROR END-IF END-IF.
```
- Host variables are prefixed with a colon; declare them in WORKING-STORAGE (a `DECLARE SECTION` is optional with the coprocessor).
- DCLGEN generates host structures and table DECLARE statements; hyphens replace underscores in COBOL names.
- `SELECT INTO` expects a single row; more raises SQLCODE -811.
- Use `WHENEVER` sparingly; explicit SQLCODE checks are clearer.

## Gotchas
- Host-variable types must match column types (DECIMAL to COMP-3, VARCHAR to a 49-level pair).
- COBOL data names containing underscores are not allowed; hyphens are.

## Self-check
Run a SELECT of a known row and a missing row; expect SQLCODE 0 and +100.
