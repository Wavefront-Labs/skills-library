---
id: computing-software.systems-network-administration.mainframe-zos.cics-statistics-and-smf110
name: cics-statistics-and-smf110
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, cics-stats, smf-110, cicsplex-sm, cics-statistics, cics-monitoring, cics-dispatch, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Measuring CICS"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Statistics and SMF 110

Goal: collect and read performance data.
- Interval and end-of-day statistics; monitoring records (class performance) in SMF 110.
- `CEMT PERFORM STATISTICS RECORD ALL`.
- Process with CICS Performance Analyzer or equivalent (confirm tool availability).
Verify: transaction CPU and response times understandable per transaction.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
