---
id: computing-software.systems-network-administration.mainframe-zos.idcams-vsam-management
name: idcams-vsam-management
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, idcams, define-cluster, repro, listcat, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Access Method Services"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IDCAMS for VSAM and catalog

Goal: manage VSAM and catalogs.
- `DEFINE CLUSTER (NAME(HLQ.KSDS) INDEXED KEYS(8 0) RECORDSIZE(80 200) VOLUMES(VOL001) CYLINDERS(5 1))`.
- `REPRO INFILE(IN) OUTFILE(OUT)`, `LISTCAT ENTRIES(x) ALL`, `DELETE x CLUSTER PURGE`, `PRINT`, `VERIFY`.
- `EXPORT`/`IMPORT` for portable copies; `ALTER` for renames and attributes.
Verify: `LISTCAT` shows records and CI splits as expected.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
