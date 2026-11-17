---
id: computing-software.systems-network-administration.mainframe-zos.cond-if-then-else
name: cond-if-then-else
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, cond-parameter, if-then-else, restart, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Step control"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# COND and IF/THEN/ELSE

Goal: control step flow.
- `//IF1 IF (STEP1.RC <= 4) THEN ... // ELSE ... // ENDIF`.
- `COND=(0,NE)` on EXEC bypasses the step if the test is true (inverse of what newcomers expect).
- Restart a failed job with `RESTART=stepname` on the JOB card (and checkpoint data as needed).
Verify: conditional steps run or skip as intended in SDSF.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
