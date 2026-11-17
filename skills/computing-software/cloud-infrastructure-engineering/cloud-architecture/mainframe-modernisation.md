---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.mainframe-modernisation
name: mainframe-modernisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, modernisation, mainframe-modernisation, legacy-modernisation, cobol, automated-refactoring]
level: advanced
status: draft
description: "Choose a mainframe and legacy modernisation path: rehost emulation, automated refactoring, replatform, rewrite or replace, with data and batch considerations."
sources: ["https://aws.amazon.com/mainframe-modernization/", "https://learn.microsoft.com/azure/architecture/mainframe/mainframe-midrange-architecture", "https://cloud.google.com/solutions/mainframe-modernization"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mainframe and legacy modernisation options

## Options
| Option | What it is | Trade-off |
|---|---|---|
| retain / integrate | keep mainframe, expose via APIs, offload reads | lowest risk, keeps MIPS cost |
| rehost (emulation) | run COBOL/PL/I/JCL on x86 with Micro Focus / Rocket Enterprise Server, NTT DATA UniKix | fast, keeps COBOL skills dependency |
| automated refactoring | tool converts COBOL to Java/C# (Blu Age, others) | modern runtime, generated code can be hard to maintain |
| rewrite | re-implement from business rules | highest cost and risk, best end state |
| replace | packaged or SaaS product | process change; good for commodity functions |

## Steps
1. **Inventory**: programs, copybooks, JCL, CICS/IMS transactions, DB2/VSAM/IMS data, batch
   schedules, MIPS consumption, integrations, unknown dead code.
2. **Segment** by business domain; choose an option per segment, not for the whole estate.
3. **Data**: EBCDIC to ASCII conversion, packed decimal (COMP-3) handling, VSAM to relational
   mapping, record layouts from copybooks; plan CDC for coexistence.
4. **Batch**: replicate the scheduler dependencies (e.g. to Control-M or a cloud workflow);
   validate batch windows on the new platform.
5. **Testing**: record-and-compare of outputs between old and new for identical inputs is the core strategy.
6. **Coexistence**: incremental migration with data sync both ways during transition.

## Gotchas
- Undocumented business rules live only in code; budget for rule extraction.
- Sort order and numeric precision differences cause subtle output mismatches.

## Verify
- [ ] Output comparison passes for full batch cycles.
- [ ] MIPS reduction and cost tracked per migrated segment.
