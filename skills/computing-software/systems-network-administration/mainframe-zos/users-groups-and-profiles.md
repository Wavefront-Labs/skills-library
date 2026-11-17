---
id: computing-software.systems-network-administration.mainframe-zos.users-groups-and-profiles
name: users-groups-and-profiles
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, adduser, addgroup, racf-userid, racf, racf-profiles, racf-classes, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Identity"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Users, groups and profiles

Goal: manage identities.
- `ADDUSER USR1 DFLTGRP(GRP1) NAME('Name') PASSWORD(<TEMP>) TSO(ACCTNUM(...)) OMVS(UID(1001) HOME(/u/usr1) PROGRAM(/bin/sh))`.
- `ALTUSER`, `LISTUSER USR1 NORACF`, `CONNECT USR1 GROUP(GRP2) AUTH(USE)`.
- Group-special/operations/auditor attributes should be rare.
Verify: user can sign on and has only intended group access.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
