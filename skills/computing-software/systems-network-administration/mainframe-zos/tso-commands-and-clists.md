---
id: computing-software.systems-network-administration.mainframe-zos.tso-commands-and-clists
name: tso-commands-and-clists
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, tso-commands, clist, rexx, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Command-line work"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TSO commands, CLIST and REXX execs

Goal: run work from TSO READY or option 6.
- `ALLOC F(IN) DA('HLQ.DATA') SHR`, `LISTCAT LEVEL(HLQ)`, `STATUS`, `SUBMIT 'HLQ.JCL(JOB1)'`, `TSO LISTDS 'HLQ.DATA' MEMBERS`.
- Store execs in a library on SYSEXEC/SYSPROC; invoke with `EX 'HLQ.EXEC(NAME)'`.
- Use `%` prefix to force exec lookup.
Verify: `LISTDS` shows the expected attributes.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
