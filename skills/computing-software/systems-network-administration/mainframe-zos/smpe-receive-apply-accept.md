---
id: computing-software.systems-network-administration.mainframe-zos.smpe-receive-apply-accept
name: smpe-receive-apply-accept
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, smpe, receive-apply-accept, hold-data, smp-e, ptf, service, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Maintenance"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SMP/E process

Goal: apply service safely.
- `RECEIVE` brings in PTFs, `APPLY CHECK` then `APPLY` installs to target libraries, `ACCEPT` to distribution libraries.
- Read HOLDDATA (ERROR, SYSTEM, FIXCAT) before applying.
- Back up with a staged copy and clone the sysres first.
Verify: `LIST` of applied PTFs and IPL test of the clone.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
