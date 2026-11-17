---
id: computing-software.systems-network-administration.mainframe-zos.capacity-and-msu
name: capacity-and-msu
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, msu, rolling-4hr-average, capacity-planning, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Cost drivers"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capacity, MSU and software cost

Goal: manage CPU cost.
- Software licensing often follows the peak rolling four-hour average of MSUs (sub-capacity pricing, confirm your contract).
- Offload eligible work to zIIP/zAAP specialty engines.
- Shift batch away from peak and tune high-CPU programs.
Verify: monthly MSU peak trends.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
