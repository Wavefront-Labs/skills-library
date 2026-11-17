---
id: computing-software.systems-network-administration.mainframe-zos.syslog-and-logrec
name: syslog-and-logrec
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, syslog, logrec, dump-analysis, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Problem diagnosis"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SYSLOG, LOGREC and diagnostics

Goal: diagnose failures.
- SYSLOG/OPERLOG hold console messages; LOGREC holds hardware/software errors (EREP).
- SVC dumps and SYSMDUMP are analysed with IPCS (`IPCS` ISPF panels).
- Message IDs (IEF…, IEC…, IGD…) tell the component; look up in z/OS MVS System Messages.
Verify: you can find the failing step's abend code and reason.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
