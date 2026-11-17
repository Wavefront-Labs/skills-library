---
id: computing-software.systems-network-administration.mainframe-zos.cics-tuning-areas
name: cics-tuning-areas
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, dsa-storage, maxtask, tcb-modes, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Resource limits"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tuning CICS regions

Goal: tune capacity.
- MXT/MAXTASKS, DSA/EDSA limits (`DSALIM`, `EDSALIM`), TCB modes (QR, L8, open API programs).
- Prefer threadsafe programs on open TCBs to reduce QR contention.
- Watch short-on-storage conditions.
Verify: no SOS/MXT messages under peak.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
