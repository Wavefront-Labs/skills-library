---
id: computing-software.systems-network-administration.mainframe-zos.db2-subsystem-and-address-spaces
name: db2-subsystem-and-address-spaces
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, ssas, dbm1, irlm, db2-zos, db2-subsystem, bufferpool, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Understanding the stack"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Db2 subsystem and address spaces

Goal: know the pieces.
- Address spaces: MSTR (system services), DBM1 (data manager), DIST (DDF), IRLM (locks), plus stored procedure address spaces.
- Catalog (DSNDB06), directory (DSNDB01), BSDS, active/archive logs.
- Commands via `-DIS DB(*)` with the command prefix.
Verify: `-DIS THREAD(*)` returns without error.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
