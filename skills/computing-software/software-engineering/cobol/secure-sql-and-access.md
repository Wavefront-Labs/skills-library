---
id: computing-software.software-engineering.cobol.secure-sql-and-access
name: secure-sql-and-access
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, secure-sql-and-access, cobol-security, sql-injection, parameter-markers, racf-access, least-privilege]
level: advanced
status: draft
description: "Avoid SQL injection in dynamic SQL and apply least privilege to datasets, DB2 and CICS resources."
sources:
  - https://www.ibm.com/docs/en/db2-for-zos
  - https://www.ibm.com/docs/en/cobol-zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dynamic SQL injection prevention and access control
**Goal:** defence in depth for COBOL applications.

- Prefer static SQL with host variables. For dynamic SQL use parameter markers:
```cobol
MOVE 'DELETE FROM T WHERE ID = ?' TO WS-STMT-TEXT
EXEC SQL PREPARE S1 FROM :WS-STMT END-EXEC
EXEC SQL EXECUTE S1 USING :WS-ID END-EXEC
```
- Never concatenate user text into SQL strings.
- On z/OS, protect datasets, DB2 plans/packages and CICS transactions/files through the external security manager (RACF, ACF2 or Top Secret); program authority comes from the job or CICS user ID, so grant the minimum required access.
- Do not embed passwords in source or JCL; use secure credential facilities (e.g. PassTickets, or vault tools your site provides).
- Mask sensitive fields in DISPLAY output and dumps; follow retention policies.

## Gotchas
- Dynamic SQL needs EXECUTE privilege on the plan plus table privileges, depending on `DYNAMICRULES`.
- Test data copied from production often violates privacy rules; mask it.

## Self-check
Try an input like `1 OR 1=1` through your dynamic SQL path; it must be treated as a literal parameter.
