---
id: computing-software.systems-network-administration.mainframe-zos.data-sharing-concepts
name: data-sharing-concepts
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, data-sharing-group, lock-structure, gbp, db2-data-sharing, group-buffer-pool, member, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Scalability"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data sharing group concepts

Goal: understand shared Db2.
- Members share data via CF structures: lock structure, SCA, group buffer pools.
- Inter-system read/write interest causes GBP-dependent pages.
- Distribute work with group attach names.
Verify: `-DIS GROUP` shows all members active.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
