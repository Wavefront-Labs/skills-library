---
id: computing-software.systems-network-administration.mainframe-zos.syncpoint-and-rollback
name: syncpoint-and-rollback
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, exec-cics-syncpoint, exec-cics-syncpoint-rollback, logical-unit-of-work, syncpoint, unit-of-work, rollback-cics, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Transaction integrity"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Syncpoint and rollback

Goal: control commit and backout.
- Implicit syncpoint at task end; `EXEC CICS SYNCPOINT` mid-task; `SYNCPOINT ROLLBACK` backs out recoverable resources.
- Recoverable files need LOG(YES)/forward recovery settings.
- Beware: syncpoint releases locks and 3270 state.
Verify: a forced abend backs out partial updates.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
