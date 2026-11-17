---
id: computing-software.systems-network-administration.mainframe-zos.sdsf-operations
name: sdsf-operations
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, sdsf, sysout, job-purge, jes2, job-class, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Working with spool"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SDSF job and output management

Goal: manage jobs and output.
- `ST` status, `H` held output, `DA` active jobs, `LOG` syslog, `I` initiators; prefix actions: `S` select, `P` purge, `C` cancel, `?` list datasets.
- `PREFIX`, `OWNER`, `SET DISPLAY` filter views.
- Operator commands via `/` prefix (`/D A,L`) if authorised.
Verify: a submitted job's JESMSGLG/JESJCL/JESYSMSG show completion codes.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
