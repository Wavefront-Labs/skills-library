---
id: computing-software.systems-network-administration.mainframe-zos.exec-cics-programming
name: exec-cics-programming
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, exec-cics-link, exec-cics-xctl, exec-cics-return, exec-cics, commarea, channels-containers, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Command level"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EXEC CICS command-level programming

Goal: write conversational and pseudo-conversational programs.
- `EXEC CICS LINK PROGRAM('P2') COMMAREA(WS-DATA) LENGTH(100)`, `XCTL`, `RETURN TRANSID('TRN2') COMMAREA(...)`.
- Check `EIBRESP` or use `RESP(WS-RESP)`; use `DFHRESP(NORMAL)` constants.
- Pseudo-conversational design releases resources between user inputs.
Verify: transaction runs and returns with a defined RESP.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
