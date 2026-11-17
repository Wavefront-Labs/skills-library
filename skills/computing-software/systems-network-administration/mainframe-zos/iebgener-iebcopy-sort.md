---
id: computing-software.systems-network-administration.mainframe-zos.iebgener-iebcopy-sort
name: iebgener-iebcopy-sort
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, iebgener, dfsort, sort-utility, idcams, iebcopy, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Copy and sort"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IEBGENER, IEBCOPY and DFSORT

Goal: copy and reorder data.
- `IEBGENER` copies sequential data (`SYSUT1`, `SYSUT2`, `SYSIN DD DUMMY`).
- `IEBCOPY` copies/compresses PDS(E) with `COPY OUTDD=...,INDD=...`.
- DFSORT/ICEMAN: `SORT FIELDS=(1,10,CH,A)`, `INCLUDE COND=`, `OUTREC BUILD=`, `SUM FIELDS=`.
Verify: record counts in SYSOUT match.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
