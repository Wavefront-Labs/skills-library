---
id: computing-software.systems-network-administration.mainframe-zos.ispf-editor-commands
name: ispf-editor-commands
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, ispf-primary-commands, line-commands, edit-macros, tso, ispf, ispf-edit, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Editing members efficiently"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ISPF editor primary and line commands

Goal: edit datasets fast in ISPF option 2.
- Primary: `FIND`/`CHANGE x y ALL`, `EXCLUDE ALL`, `RESET`, `SAVE`, `CANCEL`, `SORT`, `COPY`/`CREATE`.
- Line: `D`/`DD` delete, `I` insert, `R`/`RR` repeat, `C`/`CC` copy with `A`/`B` after/before, `M`/`MM` move, `X`/`XX` exclude, `))` shift.
- `UNDO` backs out changes; `PROFILE` shows defaults (NUMBER, CAPS, NULLS).
Verify: a multi-line change is saved and the member re-opens as expected.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
