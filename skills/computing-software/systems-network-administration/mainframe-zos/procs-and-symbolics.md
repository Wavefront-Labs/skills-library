---
id: computing-software.systems-network-administration.mainframe-zos.procs-and-symbolics
name: procs-and-symbolics
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, proc, pend, jcllib, symbolic-parameter, symbolic-parameters, cond-code, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Reusable JCL"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cataloged and in-stream procedures

Goal: reuse job steps.
- `//MYPROC PROC HLQ=PROD` ... `// PEND`; invoke `//S1 EXEC MYPROC,HLQ=TEST`.
- Override DD in a step: `//S1.INPUT DD DSN=...`; `JCLLIB ORDER=(HLQ.PROCLIB)`.
- `SET` and `&SYMBOL` for parameters; `INCLUDE MEMBER=`.
Verify: JCL expanded listing (`MSGLEVEL=(1,1)`) shows the resolved statements.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
