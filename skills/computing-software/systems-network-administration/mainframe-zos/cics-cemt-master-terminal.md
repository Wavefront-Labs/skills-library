---
id: computing-software.systems-network-administration.mainframe-zos.cics-cemt-master-terminal
name: cics-cemt-master-terminal
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, cemt, cemt-inquire, cemt-set, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Operating CICS"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CEMT master terminal commands

Goal: inquire and control resources online.
- `CEMT I TASK`, `CEMT I PROG(PGM1)`, `CEMT SET PROG(PGM1) NEWCOPY|PHASEIN`, `CEMT SET FILE(F1) CLOSED`, `CEMT P SHUT`.
- `CEMT P DUMP` and `CEMT P SHUT IMMEDIATE` are disruptive.
- Secure CEMT via RACF transaction and resource profiles.
Verify: NEWCOPY or PHASEIN loads the new program version.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
