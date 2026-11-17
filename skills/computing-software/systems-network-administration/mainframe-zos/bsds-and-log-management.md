---
id: computing-software.systems-network-administration.mainframe-zos.bsds-and-log-management
name: bsds-and-log-management
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, bsds-recovery, print-log-map, archive-log, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Logging"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BSDS and logging

Goal: manage logs.
- DSNJU003 changes BSDS; DSNJU004 (Print Log Map) reports; keep dual BSDS and logs.
- Archive log retention must cover recovery window.
- Log offload failures stall the system.
Verify: `DSNJU004` shows both copies healthy.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
