---
id: computing-software.systems-network-administration.mainframe-zos.bms-map-definition
name: bms-map-definition
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, dfhmsd, dfhmdf, mapset-assembly, bms, bms-map, send-map, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "3270 screens"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BMS mapset definition

Goal: define 3270 maps.
- Macros `DFHMSD`, `DFHMDI`, `DFHMDF` (POS, LENGTH, ATTRB, INITIAL); assemble to produce a physical map load module and a symbolic copybook.
- `SEND MAP('M1') MAPSET('S1') ERASE`, `RECEIVE MAP`; check `EIBAID` for PF keys (`DFHAID` copybook).
- Define the mapset as a CICS MAPSET resource.
Verify: screen displays and fields round-trip into the copybook.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
