---
id: computing-software.systems-network-administration.mainframe-zos.embedded-sql-cobol
name: embedded-sql-cobol
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, exec-sql, sqlca, host-variables, embedded-sql, precompile-bind, cursors, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Programming"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Embedded SQL in COBOL

Goal: write embedded SQL.
- `EXEC SQL SELECT ... INTO :HV FROM T WHERE ... END-EXEC`; check `SQLCODE` (0 ok, +100 not found, -811 multiple rows, -904 resource unavailable).
- Null indicators `:HV :IND`.
- Declare cursors with `WITH HOLD` when commit mid-loop.
Verify: all SQLCODE paths handled.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
