---
id: computing-software.systems-network-administration.mainframe-zos.jes2-classes-and-initiators
name: jes2-classes-and-initiators
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, jes2-initiator, job-class, spool-management, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Batch throughput"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JES2 job classes, initiators and spool

Goal: tune batch scheduling.
- `$D JOBCLASS(A)`, `$S I1`, `$P I1`, `$T JOBCLASS(A),MODE=...`; JES2 checkpoint and spool volumes.
- Class mapping to WLM service classes controls priority.
- Spool full conditions need purge or added volumes.
Verify: jobs flow from input to output without queuing.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
