---
id: computing-software.systems-network-administration.mainframe-zos.indexes-and-clustering
name: indexes-and-clustering
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, clustering-index, index-only-access, create-index-db2, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Index design"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Indexes and clustering

Goal: design indexes.
- `CREATE UNIQUE INDEX ... CLUSTER`; include columns for index-only access.
- Index on foreign keys; avoid over-indexing (insert cost).
- Use REORG and RUNSTATS after load to keep clustering effective.
Verify: EXPLAIN shows index access.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
