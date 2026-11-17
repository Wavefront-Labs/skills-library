---
id: computing-software.systems-network-administration.mainframe-zos.tablespace-types
name: tablespace-types
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, universal-tablespace, partition-by-range, partition-by-growth, tablespace, db2-ddl, partitioned-tablespace, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Storage design"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Table space types

Goal: choose a tablespace type.
- Universal table spaces (PBG or PBR) are the standard now; segmented/simple/classic partitioned are legacy.
- `CREATE TABLESPACE TS1 IN DB1 MAXPARTITIONS 10 SEGSIZE 32 ...`.
- Partition for utility parallelism and data aging.
Verify: `SYSIBM.SYSTABLESPACE` reflects the type.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
