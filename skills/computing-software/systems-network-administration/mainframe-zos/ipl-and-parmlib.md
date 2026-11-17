---
id: computing-software.systems-network-administration.mainframe-zos.ipl-and-parmlib
name: ipl-and-parmlib
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, ipl-process, parmlib, loadxx, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "System start-up"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IPL and PARMLIB

Goal: understand how z/OS starts.
- IPL loads from the sysres via LOADxx which points to IEASYSxx and PARMLIB concatenation; master catalog and nucleus load.
- PARMLIB members configure everything (IEASYSxx, PROGxx, COMMNDxx, SMFPRMxx).
- Test changes with `T` commands and `SETLOAD`; keep fallback members.
Verify: system comes up with the intended members (`D IPLINFO`).

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
