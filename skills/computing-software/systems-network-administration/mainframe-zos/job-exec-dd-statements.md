---
id: computing-software.systems-network-administration.mainframe-zos.job-exec-dd-statements
name: job-exec-dd-statements
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, jcl-job-card, dd-statement, jcl-syntax, jcl, job-statement, exec-pgm, mainframe, zos, ibm-z]
level: practitioner
status: draft
description: "Core statements"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JOB, EXEC and DD statements

Goal: write a valid job.
- `//NAME JOB (acct),'user',CLASS=A,MSGCLASS=X,NOTIFY=&SYSUID`; `//STEP1 EXEC PGM=IEBGENER`; `//SYSUT1 DD DSN=HLQ.IN,DISP=SHR`.
- Columns: `//` in 1-2, name from col 3, then operation, operands, comments after a space; continue after a comma.
- `/*` delimiter ends in-stream data; `//*` is a comment.
Verify: submit and read RC=0000 in SDSF.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
