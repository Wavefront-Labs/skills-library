---
id: computing-software.systems-network-administration.mainframe-zos.le-runtime-options
name: le-runtime-options
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, cee-options, runopts, ceedump, language-environment, compile-cobol, link-edit, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "LE settings"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Language Environment runtime options

Goal: tune LE.
- `CEEOPTS DD`, `//STEP EXEC PGM=X,PARM='/RPTOPTS(ON)'`; `TRAP(ON)`, `ABTERMENC(ABEND)`, `HEAP`, `STACK`, `RPTSTG`.
- `CEEDUMP` shows traceback; `CEE3DMP` calls for a dump.
- Standardise options via CEEDOPT/CEEROPT.
Verify: RPTOPTS output matches the intended settings.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
