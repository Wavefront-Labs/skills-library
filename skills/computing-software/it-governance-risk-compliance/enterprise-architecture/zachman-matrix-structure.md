---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.zachman-matrix-structure
name: zachman-matrix-structure
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [zachman-matrix-structure, zachman-framework, zachman, zachman framework, 6x6 matrix, interrogatives, what how where who when why, perspectives, enterprise-architecture]
level: intro
status: draft
description: "Read the Zachman enterprise ontology: six interrogatives by six audience perspectives, and what each cell holds."
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

# Zachman 6x6 classification schema

Goal: use Zachman as a classification, not a process.

- Columns (interrogatives): What (inventory), How (process), Where (distribution), Who (responsibility), When (timing), Why (motivation).
- Rows (perspectives): Executive/Scope (contextual), Business Management (conceptual), Architect (logical), Engineer (physical), Technician (as built), Enterprise (operating instance); names vary by version (confirm the current naming on the Zachman site).
- Each cell holds one primitive model; composite models combine cells.
- Rules: columns have no order; each cell is unique; do not fill a cell by mixing columns.

Gotchas:
- It is a schema for completeness, not a method; pair it with an approach like TOGAF.

Verify: you can place any artifact in exactly one cell.
