---
id: computing-software.systems-network-administration.mainframe-zos.db2-commands-and-restart
name: db2-commands-and-restart
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, dis-thread, start-db2, term-utility, db2-commands, bsds, db2-logging, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Operating"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Db2 commands and restart

Goal: operate Db2.
- `-DIS DB(DB1) SPACENAM(*) RESTRICT`, `-START DB(DB1) SPACENAM(TS1)`, `-DIS UTILITY(*)`, `-TERM UTILITY(id)`, `-STOP DDF MODE(QUIESCE)`.
- Restricted states (COPY pending, REORP, CHKP) need specific utilities to clear.
- Restart after failure replays logs automatically.
Verify: restricted objects cleared.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
