---
id: computing-software.systems-network-administration.mainframe-zos.rmf-monitoring
name: rmf-monitoring
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, rmf-reports, cpu-utilization, delay-reports, rmf, rmf-monitor-iii, capacity, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Performance data"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RMF Monitor I/III

Goal: monitor z/OS.
- Monitor III shows delays (CPU, storage, device, ENQ) by job; Monitor I interval reports go to SMF 70-79.
- Postprocessor produces CPU, workload, coupling facility reports.
- Compare against WLM goals.
Verify: key jobs' delay reasons identified.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
