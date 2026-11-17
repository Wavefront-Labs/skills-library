---
id: computing-software.systems-network-administration.mainframe-zos.workload-manager-wlm
name: workload-manager-wlm
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, wlm, service-class, goals, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Performance policy"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Workload Manager

Goal: set goals for work.
- WLM service policy defines service classes with importance, velocity or response-time goals, plus classification rules mapping work to classes.
- Install and activate with `V WLM,POLICY=name`.
- Check with RMF (Monitor III) performance index (PI < 1 means goal met).
Verify: key services achieve PI near or under 1.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
