---
id: computing-software.systems-network-administration.mainframe-zos.cics-resource-security
name: cics-resource-security
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, xtran, xfct, resource-security, cics-security, sit-sec, transaction-security, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Securing CICS"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transaction and resource security

Goal: secure CICS resources.
- SIT `SEC=YES`, `XTRAN=YES`, `XFCT=YES`, `XDB2=YES`; RACF classes `TCICSTRN`, `GCICSTRN`, `FCICSFCT`.
- Profiles per transaction or file; grant READ to groups.
- Userid propagation to Db2 via plan/package authorisation.
Verify: unauthorised user receives a security error (e.g., ATNI/AEY7).

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
