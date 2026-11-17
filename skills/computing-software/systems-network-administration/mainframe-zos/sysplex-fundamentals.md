---
id: computing-software.systems-network-administration.mainframe-zos.sysplex-fundamentals
name: sysplex-fundamentals
category: computing-software
field: systems-network-administration
product: mainframe-zos
tags: [mainframe-zos, parallel-sysplex, cf-structures, xcf-signalling, sysplex, coupling-facility, xcf, mainframe, zos, ibm-z, jcl]
level: practitioner
status: draft
description: "Clustering"
sources: ["https://www.ibm.com/docs/en/zos", "https://www.ibm.com/docs/en/cics-ts", "https://www.ibm.com/docs/en/db2-for-zos", "https://www.ibm.com/docs/en/zos/latest?topic=security-racf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parallel Sysplex fundamentals

Goal: understand mainframe clustering.
- Sysplex = multiple LPARs/systems with shared time (STP), couple datasets, and a Coupling Facility for lock, list and cache structures.
- `D XCF,S,ALL` shows members; `D XCF,STR` shows structures.
- GRS, VTAM generic resources and Db2/CICS data sharing exploit CF.
Verify: `D XCF,S,ALL` lists all systems ACTIVE.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
