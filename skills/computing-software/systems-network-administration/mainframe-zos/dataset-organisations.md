---
id: computing-software.systems-network-administration.mainframe-zos.dataset-organisations
name: dataset-organisations
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, dsorg, pdse, partitioned-dataset, dataset, pds, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Choosing a format"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dataset organisations (PS, PDS, PDSE, VSAM)

Goal: pick and allocate the right organisation.
- PS (sequential), PO (PDS/PDSE library with members), DA, VSAM (KSDS, ESDS, RRDS, LDS), HFS/zFS in UNIX.
- PDSE advantages: no compress, dynamic directory; PDS needs periodic compress (`=3.1` Z or IEBCOPY).
- Allocate with RECFM, LRECL, BLKSIZE (usually system-determined, `BLKSIZE=0`), SPACE.
Verify: `LISTDS` shows DSORG, RECFM, LRECL as designed.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
