---
id: computing-software.systems-network-administration.mainframe-zos.dataset-profile-protection
name: dataset-profile-protection
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, addsd, permit, universal-access, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Protecting datasets"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dataset profiles and access

Goal: protect data.
- `ADDSD 'HLQ.**' UACC(NONE)`, `PERMIT 'HLQ.**' ID(GRP1) ACCESS(UPDATE)`, `LISTDSD DATASET('HLQ.X') ALL`.
- Generic profiles; most specific match wins. `SETROPTS GENERIC(DATASET) REFRESH`.
- Use `RACLIST` for general resource classes to cache in storage.
Verify: `LISTDSD` and a test access check match intent.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
