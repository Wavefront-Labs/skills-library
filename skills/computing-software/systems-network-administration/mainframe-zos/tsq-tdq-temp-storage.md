---
id: computing-software.systems-network-administration.mainframe-zos.tsq-tdq-temp-storage
name: tsq-tdq-temp-storage
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, tsq, tdq, writeq-ts, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Queues"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Temporary storage and transient data

Goal: use queues for work and passing.
- TS queue: `WRITEQ TS QUEUE('Q1') FROM() ITEM()`, `READQ TS`, `DELETEQ TS`; main or auxiliary storage.
- TD queue: intrapartition (triggerable) vs extrapartition (sequential datasets).
- Size TS pools; delete queues to avoid leaks.
Verify: queue contents readable and deleted after use.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
