---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.change-management-process
name: change-management-process
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [change-management-process, adm-phase-h-change, phase h, change request, architecture change management, simplification change, incremental change, re-architecting change, change classification, enterprise-architecture]
level: practitioner
status: draft
description: "Monitor technology and business change, classify requests as simplification, incremental or re-architecting, and decide whether to open a new ADM cycle."
sources:
  - https://pubs.opengroup.org/togaf-standard/
  - https://pubs.opengroup.org/architecture/archimate32-doc/
  - https://www.zachman.com/about-the-zachman-framework
  - https://www.businessarchitectureguild.org/
  - https://www.dodcio.defense.gov/Library/DoD-Architecture-Framework/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture change management process

Goal: keep the architecture current without constant redesign.

- Classify each change: simplification (handle by maintenance), incremental (handle by change management), re-architecting (start a new ADM cycle).
- Use drivers for change: new technology, business change, regulation, lessons learned.
- Run a change board with criteria for acceptance and impact analysis.
- Update repository, catalogs and roadmap after each decision.

Gotchas:
- Without a classification rule everything becomes a big redesign.
- Track dispensations that should become requirements.

Verify: every change request has a class, decision and updated repository entry.
