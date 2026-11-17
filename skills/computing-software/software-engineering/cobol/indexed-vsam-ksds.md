---
id: computing-software.software-engineering.cobol.indexed-vsam-ksds
name: indexed-vsam-ksds
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, indexed-vsam-ksds, cobol-indexed-relative, indexed-file, record-key, alternate-key, vsam-ksds]
level: practitioner
status: draft
description: "Define indexed file access with prime and alternate keys; map to VSAM KSDS on z/OS and ISAM libraries in GnuCOBOL."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# INDEXED files with RECORD KEY and ALTERNATE KEY (VSAM KSDS)
**Goal:** keyed access by one or more fields.

```cobol
SELECT CUST ASSIGN TO CUSTVSAM
    ORGANIZATION IS INDEXED
    ACCESS MODE IS DYNAMIC
    RECORD KEY IS CUST-ID
    ALTERNATE RECORD KEY IS CUST-ZIP WITH DUPLICATES
    FILE STATUS IS WS-FS WS-VSAM-FS.
```
- The RECORD KEY must be inside the record and unique; the alternate key may allow duplicates.
- z/OS: the cluster is defined with IDCAMS (see the VSAM topic); the program does not create indexes.
- GnuCOBOL: depends on the build (Berkeley DB, VBISAM, C-ISAM or built-in); the on-disk format is not compatible with VSAM.

## Gotchas
- Changing a record's primary key by REWRITE is not allowed (status 21); DELETE then WRITE.
- Alternate-key indexes slow down WRITE and REWRITE.

## Self-check
Write three records, read them back by alternate key, and confirm duplicates appear in key order.
