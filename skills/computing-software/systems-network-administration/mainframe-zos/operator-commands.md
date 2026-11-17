---
id: computing-software.systems-network-administration.mainframe-zos.operator-commands
name: operator-commands
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, display-commands, vary-command, console-commands, operator-commands, console, ipl, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Operating a system"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MVS operator commands

Goal: monitor and control z/OS.
- `D A,L` active units, `D T` time, `D M=CPU`, `D U,,,addr`, `V addr,ONLINE`, `F jobname,...` modify, `P jobname` stop, `C jobname` cancel.
- Console authority via RACF OPERCMDS profiles.
- Use `SETPROG`, `T PROG=xx` for dynamic changes.
Verify: command output matches expected state.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
