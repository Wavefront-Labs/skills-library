---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.data-catalogs-and-diagrams
name: data-catalogs-and-diagrams
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [data-catalogs-and-diagrams, adm-phase-c-data, data entity catalog, data entity business function matrix, conceptual data diagram, logical data diagram, data dissemination diagram, data lifecycle diagram, data security diagram, enterprise-architecture]
level: practitioner
status: draft
description: "Produce the Phase C data artifacts: entity catalog, data entity to business function matrix, conceptual and logical data diagrams, data dissemination and security views."
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

# Data architecture catalogs, matrices and diagrams

Goal: pick the data artifacts that answer stakeholder concerns.

- Catalog: Data Entity/Data Component.
- Matrix: Data Entity/Business Function; Application/Data.
- Diagrams: Conceptual Data, Logical Data, Data Dissemination, Data Security, Data Migration, Data Lifecycle.

Use the Application/Data matrix to show which application creates, reads, updates or deletes each entity (CRUD).

Gotchas:
- Conceptual and logical models serve different audiences; do not merge them.
- Data migration diagrams belong to the transition planning, not only the target.

Verify: CRUD matrix has exactly one creating system per entity.
