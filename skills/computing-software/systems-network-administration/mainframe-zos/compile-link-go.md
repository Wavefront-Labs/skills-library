---
id: computing-software.systems-network-administration.mainframe-zos.compile-link-go
name: compile-link-go
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, prelink-binder, compile-jcl, load-module, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Build chain"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compile, link-edit and run

Goal: build executables.
- Compile with the language compiler proc (e.g., `IGYWCL`), binder (IEWL/`HEWL`) into a load library or PDSE program object; STEPLIB/JOBLIB at run time.
- Options: `LIST`, `MAP`, `OFFSET`, `OPT`; binder `NCAL`, `RENT`, `AMODE/RMODE`.
- Understand LINKLIST/LPA for system-wide modules.
Verify: program executes from the load library with RC=0.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
