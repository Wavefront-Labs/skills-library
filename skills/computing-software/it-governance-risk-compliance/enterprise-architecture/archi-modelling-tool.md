---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archi-modelling-tool
name: archi-modelling-tool
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archi-modelling-tool, ea-tooling, archi, archimate tool, jarchi, open exchange format, csv import, model tree, views, enterprise-architecture]
level: practitioner
status: draft
description: "Create ArchiMate models in Archi with views, properties, specializations, scripting via jArchi and export to CSV or Open Exchange."
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

# Archi: open-source ArchiMate modelling

Goal: productive use of Archi.

- Model tree holds elements and relationships; diagrams (views) reference them.
- Palette creates elements; Properties tab holds documentation, properties and specialization.
- Export: File > Export > Model to CSV, Open Exchange XML, or HTML report.
- Import: CSV (elements, relations, properties files) or Open Exchange.
- Scripting: the jArchi plugin runs JavaScript to automate edits.
- Store models in Git by saving the .archimate file (consider the coArchi plugin for collaboration).

Gotchas:
- Keep one element per concept; reuse via the tree, do not copy-paste.
- Plugins vary by version; confirm compatibility.

Verify: opening the exported report shows each view and element documentation.
