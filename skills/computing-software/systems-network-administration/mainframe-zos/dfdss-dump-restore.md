---
id: computing-software.systems-network-administration.mainframe-zos.dfdss-dump-restore
name: dfdss-dump-restore
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, adrdssu, dss-dump, dss-restore, dfhsm, dfdss, hsm-migrate, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Volume and dataset backup"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DFSMSdss dump and restore

Goal: back up datasets and volumes.
- `ADRDSSU` with `DUMP DATASET(INCLUDE(HLQ.**)) OUTDD(DUMP) ...` and `RESTORE`; `COPY`, `DEFRAG`, `COMPRESS`.
- Use `TOL(ENQF)` and `ALLDATA(*)` as needed.
- Store backups off site.
Verify: restore to alternate names matches source.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
