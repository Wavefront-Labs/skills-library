---
id: computing-software.systems-network-administration.mainframe-zos.terminal-and-3270-attributes
name: terminal-and-3270-attributes
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, field-attributes, cursor-positioning, mdt, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Screen behaviour"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 3270 data stream and attribute handling

Goal: handle fields correctly.
- Attributes: protected/unprotected, bright, hidden, auto-skip; MDT determines which fields are returned.
- Use `CURSOR(offset)` or `-1` length conventions; `DFHBMFSE` for modified.
- Test on a real 3270 emulator.
Verify: modified fields only return as expected.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
