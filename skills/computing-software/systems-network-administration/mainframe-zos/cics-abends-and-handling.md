---
id: computing-software.systems-network-administration.mainframe-zos.cics-abends-and-handling
name: cics-abends-and-handling
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, handle-abend, abend-codes, asra, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Diagnosing failures"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CICS abends and error handling

Goal: interpret and handle abends.
- `ASRA` program check (like S0C7/S0C4), `AEI0`-`AEIZ` command errors (`AEIO` = NOTOPEN etc.), `AICA` runaway task.
- `EXEC CICS HANDLE ABEND LABEL()/PROGRAM()` and `ABEND ABCODE('XXXX')`.
- Dumps go to dump datasets (`CEMT P DUMP`).
Verify: abend code matched to cause via the CICS messages manual.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
