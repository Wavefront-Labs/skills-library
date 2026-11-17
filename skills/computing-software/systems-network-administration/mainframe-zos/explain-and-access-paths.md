---
id: computing-software.systems-network-administration.mainframe-zos.explain-and-access-paths
name: explain-and-access-paths
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, explain-plan-table, access-path-tuning, optimizer-hints, explain, access-path, db2-locking, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Query tuning"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EXPLAIN and access paths

Goal: understand access paths.
- `EXPLAIN PLAN SET QUERYNO=1 FOR SELECT ...` fills `PLAN_TABLE`; read ACCESSTYPE (I, R, M), MATCHCOLS, PREFETCH.
- Use accurate statistics; avoid optimizer hints unless required.
- Data Studio / tools visualise plans.
Verify: matching columns and index use as designed.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
