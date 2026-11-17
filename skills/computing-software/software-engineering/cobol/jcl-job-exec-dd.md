---
id: computing-software.software-engineering.cobol.jcl-job-exec-dd
name: jcl-job-exec-dd
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, jcl-job-exec-dd, cobol-jcl, job-statement, exec-pgm, dd-statement, stepdd]
level: intro
status: draft
description: "Read and write the three core JCL statements to run a COBOL load module with its files."
sources:
  - https://www.ibm.com/docs/en/zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JOB, EXEC and DD statements
**Goal:** a correct batch job for a COBOL step.

```jcl
//MYJOB   JOB (ACCT),'NIGHTLY',CLASS=A,MSGCLASS=X,MSGLEVEL=(1,1)
//STEP1   EXEC PGM=CUSTUPD,PARM='2025-11-02'
//STEPLIB DD DSN=<USER>.LOADLIB,DISP=SHR
//CUSTIN  DD DSN=<USER>.CUST.MASTER,DISP=SHR
//CUSTOUT DD DSN=<USER>.CUST.NEW,DISP=(NEW,CATLG,DELETE),
//           SPACE=(CYL,(10,5),RLSE),DCB=(RECFM=FB,LRECL=100,BLKSIZE=0)
//SYSOUT  DD SYSOUT=*
//SYSIN   DD *
 CARD DATA
/*
```
- The DD name matches the `ASSIGN TO` name in the COBOL SELECT.
- `PARM` arrives as a halfword length plus text in the LINKAGE SECTION.
- `SYSOUT=*` routes to the job's output; `DD *` is inline input; `DD DUMMY` supplies an empty file.
- `//stepname.ddname DD ...` overrides in a procedure.

## Gotchas
- A column-72 overrun in JCL is a syntax error; continue with a comma and `//` in columns 1-2.
- DD names are limited to 8 characters.

## Self-check
Submit with each DD and verify the step ends RC=0 and CUSTOUT is cataloged.
