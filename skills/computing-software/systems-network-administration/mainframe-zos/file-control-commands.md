---
id: computing-software.systems-network-administration.mainframe-zos.file-control-commands
name: file-control-commands
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, exec-cics-read, exec-cics-write, exec-cics-rewrite, cics-file-control, vsam-in-cics, read-for-update, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "VSAM access"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# File control commands

Goal: read and update VSAM from CICS.
- `READ FILE('F') INTO() RIDFLD() UPDATE`, `REWRITE`, `WRITE`, `DELETE`, browse with `STARTBR/READNEXT/ENDBR`.
- Conditions: NOTFND, DUPREC, ENDFILE, NOTOPEN.
- RLS vs LSR/NSR; define file resource attributes accordingly.
Verify: update commits at syncpoint and holds enqueue until then.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
