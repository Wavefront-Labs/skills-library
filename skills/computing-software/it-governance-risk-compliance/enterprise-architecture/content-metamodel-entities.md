---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.content-metamodel-entities
name: content-metamodel-entities
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [content-metamodel-entities, architecture-content-framework, content metamodel, metamodel entities, core metamodel, metamodel extensions, architecture content, enterprise-architecture]
level: practitioner
status: draft
description: "Use the TOGAF content metamodel (core plus extensions) to keep artifacts consistent across catalogs, matrices and diagrams."
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

# Content metamodel entities and relationships

Goal: define entities and relationships once and generate views from them.

- Core metamodel covers entities such as actor, role, business service, process, function, data entity, application component, technology component and their relations.
- Extensions add governance, services, process modelling, data, infrastructure consolidation and motivation.
- Adopt the subset you need, and map it to the tool (ArchiMate maps well).
- Define naming and ID rules.

Gotchas:
- Adopting the full metamodel without need creates data entry overhead.
- Extend, do not fork; keep mapping to the original.

Verify: each artifact in use maps to metamodel entities.
