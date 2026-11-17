---
id: computing-software.software-engineering.cobol.idcams-define-cluster
name: idcams-define-cluster
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, idcams-define-cluster, cobol-vsam, idcams, define-cluster, repro, listcat]
level: advanced
status: draft
description: "Create and load VSAM KSDS clusters used by COBOL INDEXED files with IDCAMS."
sources:
  - https://www.ibm.com/docs/en/zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IDCAMS DEFINE CLUSTER, REPRO and LISTCAT
**Goal:** a ready VSAM file for the program.

```jcl
//DEFINE EXEC PGM=IDCAMS
//SYSPRINT DD SYSOUT=*
//SYSIN DD *
  DEFINE CLUSTER (NAME(<USER>.CUST.KSDS) -
     INDEXED KEYS(6 0) RECORDSIZE(100 100) -
     CYLINDERS(5 1) FREESPACE(10 10) SHAREOPTIONS(2 3)) -
   DATA (NAME(<USER>.CUST.KSDS.DATA)) -
   INDEX (NAME(<USER>.CUST.KSDS.INDEX))
  REPRO INFILE(SEQIN) OUTDATASET(<USER>.CUST.KSDS)
  LISTCAT ENTRIES(<USER>.CUST.KSDS) ALL
/*
```
- `KEYS(len offset)` must match the COBOL RECORD KEY length and position.
- REPRO loads in key order (from a sorted sequential file); unsorted input fails for KSDS.
- Hyphen at line end continues IDCAMS commands.
- File status 9x from COBOL on VSAM comes with a VSAM return/feedback code in the extended FILE STATUS.

## Gotchas
- Mismatch between cluster RECORDSIZE and the program's record length gives status 39/4x errors.
- DELETE CLUSTER before redefine in reruns; add `SET MAXCC=0` guard when rerunning.

## Self-check
LISTCAT shows the KEYLEN/RKP you intended; REPRO count equals input count.
