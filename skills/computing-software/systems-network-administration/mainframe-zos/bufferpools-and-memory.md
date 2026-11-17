---
id: computing-software.systems-network-administration.mainframe-zos.bufferpools-and-memory
name: bufferpools-and-memory
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, bufferpool-tuning, alter-bufferpool, hit-ratio, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Memory tuning"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Buffer pools

Goal: tune buffer pools.
- `-ALTER BUFFERPOOL(BP1) VPSIZE(50000)`; separate indexes, tables, work files.
- Hit ratio and sequential thresholds (VPSEQT) matter.
- Use page fixing (PGFIX) for I/O reduction.
Verify: hit ratios and synchronous reads improve.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
