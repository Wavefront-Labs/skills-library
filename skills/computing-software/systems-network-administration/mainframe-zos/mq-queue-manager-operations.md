---
id: computing-software.systems-network-administration.mainframe-zos.mq-queue-manager-operations
name: mq-queue-manager-operations
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, mq-zos, runmqsc, csqutil, ibm-mq-zos, ims-db, ims-tm, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Messaging"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MQ queue manager operations

Goal: operate MQ on z/OS.
- Commands with prefix: `-MQ1 DISPLAY QLOCAL(*) CURDEPTH`, `DEFINE QLOCAL(Q1) MAXDEPTH(5000)`.
- Page sets, buffer pools, logs, CSQUTIL for backup and copy.
- Shared queues use the CF.
Verify: put and get test messages succeed.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
