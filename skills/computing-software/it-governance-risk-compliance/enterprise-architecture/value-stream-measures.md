---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.value-stream-measures
name: value-stream-measures
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [value-stream-measures, value-streams, lead time, value stream metrics, information map, information concept, flow efficiency, bizbok information map, enterprise-architecture]
level: advanced
status: draft
description: "Attach lead time, cost and quality measures to stages and link to information concepts in an information map."
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

# Value stream metrics and information maps

Goal: manage the stream with data.

- Measure per stage: lead time, process time, cost, quality (defect rate).
- Compute flow efficiency = process time / lead time.
- Information map: list business information concepts (customer, order) and relationships, independent of systems.
- Link information concepts to stages that create or use them.

Gotchas:
- Measure where the pain is; do not instrument everything.

Verify: baseline and target values recorded for at least the critical stages.
