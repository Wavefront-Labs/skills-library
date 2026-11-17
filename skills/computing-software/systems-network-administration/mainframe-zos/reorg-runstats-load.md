---
id: computing-software.systems-network-administration.mainframe-zos.reorg-runstats-load
name: reorg-runstats-load
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, reorg-tablespace, runstats-utility, load-utility, db2-reorg, db2-runstats, db2-load, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Regular maintenance"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# REORG, RUNSTATS and LOAD

Goal: keep data organised.
- `REORG TABLESPACE DB1.TS1 SHRLEVEL CHANGE`, `RUNSTATS TABLESPACE ... TABLE(ALL) INDEX(ALL)`, `LOAD DATA RESUME YES INTO TABLE T`.
- Run via DSNUTILB JCL or the DSNUPROC proc; monitor with `-DIS UTILITY(*)`.
- Use real-time statistics to decide when to reorg.
Verify: REORG ends RC=0 and statistics updated.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
