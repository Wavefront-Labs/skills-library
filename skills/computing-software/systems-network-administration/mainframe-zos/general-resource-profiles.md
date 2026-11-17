---
id: computing-software.systems-network-administration.mainframe-zos.general-resource-profiles
name: general-resource-profiles
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, rdefine, rlist, racf-class-active, general-resource-class, setropts, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "FACILITY, OPERCMDS, SURROGAT etc."
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# General resource profiles

Goal: protect non-dataset resources.
- `RDEFINE FACILITY BPX.SUPERUSER UACC(NONE)`, `PERMIT ... CLASS(FACILITY) ID(x) ACCESS(READ)`, `SETROPTS RACLIST(FACILITY) REFRESH`.
- Classes: TSOPROC, OPERCMDS, PROGRAM, XFACILIT, STARTED, DIGTCERT, CICS classes.
- Activate classes with `SETROPTS CLASSACT(class)`.
Verify: `RLIST class profile ALL` shows the access list.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
