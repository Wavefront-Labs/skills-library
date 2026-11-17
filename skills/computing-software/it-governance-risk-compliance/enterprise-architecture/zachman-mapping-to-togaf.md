---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.zachman-mapping-to-togaf
name: zachman-mapping-to-togaf
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [zachman-mapping-to-togaf, zachman-framework, zachman to togaf, completeness check, artifact mapping, coverage analysis, gap in views, enterprise-architecture]
level: practitioner
status: draft
description: "Use the Zachman schema to find missing views by mapping existing TOGAF or ArchiMate artifacts to cells."
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

# Map Zachman cells to TOGAF artifacts and use as a completeness check

Goal: find what you have not modelled.

1. Build a grid of the 36 cells.
2. Place each existing artifact in its cell (for example a business footprint diagram under Business Management x Where).
3. Mark empty cells as gaps and decide if they matter for stakeholders.
4. Do not fill all cells for the sake of it; fill those with concerns.
5. Record the result as a coverage view in the repository.

Gotchas:
- Cells empty by design should be marked "not needed" so the next reviewer knows.

Verify: coverage matrix reviewed with the sponsor and updated yearly.
