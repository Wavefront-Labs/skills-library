---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.sparx-ea-modelling
name: sparx-ea-modelling
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [sparx-ea-modelling, ea-tooling, sparx ea, enterprise architect, sparx systems, project browser, mdg technology, baselines, shared repository, ea model, enterprise-architecture]
level: practitioner
status: draft
description: "Use Sparx EA with ArchiMate and UML/SysML, project browser, shared repositories, baselines and model transformations."
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

# Sparx Enterprise Architect for EA and repository modelling

Goal: use EA as a shared model repository.

- Models are stored in .eap/.eapx files or a shared database repository (SQL Server, PostgreSQL and others; confirm supported versions).
- Enable the ArchiMate or TOGAF technologies (MDG) in the Technologies manager.
- Use packages for domains, baselines for versions, and security for permissions.
- Create diagrams and use Model Transformation or Document Generator for outputs.
- Use Relationship Matrix and Model Views for reporting.

Gotchas:
- Define package structure and naming up front.
- File-based repositories do not scale to many editors.

Verify: a baseline can be restored and compared.
