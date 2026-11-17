---
id: computing-software.systems-network-administration.mainframe-zos.native-encryption-and-masking
name: native-encryption-and-masking
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, row-permission, column-mask, db2-encryption, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Fine-grained access"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Row permissions and column masks

Goal: add data protection.
- `CREATE PERMISSION` and `CREATE MASK`; activate row/column access control on the table.
- Data set encryption via DFSMS plus RACF key labels (confirm).
- Test with various authids.
Verify: unprivileged id sees masked data.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
