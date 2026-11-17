---
id: computing-software.systems-network-administration.mainframe-zos.started-tasks-and-surrogat
name: started-tasks-and-surrogat
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, started-task-identity, surrogat-class, batch-userid, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Identity for started work"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# STARTED class and SURROGAT

Goal: give started tasks the right identity.
- `RDEFINE STARTED MYSTC.* STDATA(USER(STCUSER) GROUP(STCGRP) TRUSTED(NO))`.
- SURROGAT profiles (`BPX.SRV.userid`, `userid.SUBMIT`) allow submitting under another id.
- Protected user IDs (NOPASSWORD) for started tasks.
Verify: started task runs with the intended user.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
