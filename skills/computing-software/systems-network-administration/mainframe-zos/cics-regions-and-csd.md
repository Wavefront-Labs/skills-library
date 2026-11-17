---
id: computing-software.systems-network-administration.mainframe-zos.cics-regions-and-csd
name: cics-regions-and-csd
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, cics-csd, ceda, cics-startup, cics, cics-region, cics-resource-definitions, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Defining resources"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CICS regions, CSD and resource definitions

Goal: define and install CICS resources.
- Resources (PROGRAM, TRANSACTION, FILE, TDQUEUE, TSMODEL, LIBRARY) live in the CSD (managed with `CEDA`/`DFHCSDUP`) or in CPSM/BAS.
- `CEDA DEFINE TRANSACTION(TRN1) PROGRAM(PGM1) GROUP(MYGRP)` then `CEDA INSTALL GROUP(MYGRP)`.
- Startup types: INITIAL, COLD, AUTO, WARM, EMERGENCY (SIT `START=`).
Verify: `CEMT I TRAN(TRN1)` shows ENABLED.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
