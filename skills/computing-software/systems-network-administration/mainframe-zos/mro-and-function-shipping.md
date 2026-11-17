---
id: computing-software.systems-network-administration.mainframe-zos.mro-and-function-shipping
name: mro-and-function-shipping
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, mro, function-shipping, dynamic-routing, isc, cicsplex-sm, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Multiple regions"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MRO and function shipping

Goal: split work across regions.
- TOR/AOR/FOR topology: terminal-owning, application-owning, file-owning regions.
- Remote resources defined with `REMOTESYSTEM`; connections via IRC/XCF.
- Dynamic routing (CPSM WLM) balances AORs.
Verify: a transaction runs on an AOR via the TOR.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
