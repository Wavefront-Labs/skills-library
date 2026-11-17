---
id: computing-software.systems-network-administration.mainframe-zos.ims-overview
name: ims-overview
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, ims-dl1, ims-transaction-manager, psb-dbd, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Hierarchical database and TM"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IMS DB and TM overview

Goal: recognise IMS concepts.
- DBD describes databases; PSB describes program views; segments in hierarchies; DL/I calls (`GU`, `GN`, `ISRT`, `REPL`, `DLET`).
- IMS TM schedules message-driven transactions.
- Modern access via IMS Connect and open APIs (confirm).
Verify: DL/I call status codes understood (blank = OK, GE = not found).

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
