---
id: computing-software.systems-network-administration.mainframe-zos.gdg-generation-data-groups
name: gdg-generation-data-groups
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, gdg, gdg-base, generation-limit, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Versioned datasets"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generation data groups

Goal: manage versioned files.
- `DEFINE GDG (NAME(HLQ.GDG) LIMIT(7) SCRATCH NOEMPTY)`; reference `HLQ.GDG(0)`, `(+1)`, `(-1)`.
- `(+1)` in several steps refers to the same new generation within a job.
- Limit and EMPTY/SCRATCH control rolloff.
Verify: `LISTCAT` shows generations cycling.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
