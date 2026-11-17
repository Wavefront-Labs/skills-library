---
id: computing-software.systems-network-administration.mainframe-zos.bind-plans-packages
name: bind-plans-packages
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, bind-package, bind-plan, collection-id, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Access path binding"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Packages, plans and BIND

Goal: manage static SQL binds.
- Precompile (or coprocessor) produces DBRM; `BIND PACKAGE(COLL) MEMBER(PGM1) ISOLATION(CS) CURRENTDATA(NO)`.
- Rebind after RUNSTATS to refresh access paths; use plan management (`PLANMGMT`) to fall back.
- Explicit `ISOLATION` and `RELEASE(COMMIT)` choices affect locking.
Verify: `SYSIBM.SYSPACKAGE` shows the new version.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
