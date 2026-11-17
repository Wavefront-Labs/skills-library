---
id: computing-software.systems-network-administration.mainframe-zos.smf-recording-setup
name: smf-recording-setup
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, smf-dump, smfprmxx, smf-types, smf, smf-records, syslog, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Collecting records"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SMF recording configuration

Goal: collect system accounting.
- SMFPRMxx selects record types and intervals; dump with `IFASMFDP` JCL (`DUMP INDD(...) OUTDD(...)`).
- Common types: 30 (job), 70-79 (RMF), 80 (RACF), 110 (CICS), 100-102 (Db2).
- Store dumps off-system for audit retention.
Verify: records of the expected types appear in a dump.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
