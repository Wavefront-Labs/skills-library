---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.application-catalogs-and-diagrams
name: application-catalogs-and-diagrams
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [application-catalogs-and-diagrams, adm-phase-c-application, application portfolio catalog, interface catalog, application interaction matrix, application communication diagram, application use case diagram, enterprise manageability diagram, enterprise-architecture]
level: practitioner
status: draft
description: "Produce Phase C application artifacts: application portfolio catalog, interface catalog, interaction matrix, communication, cooperation and software engineering diagrams."
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

# Application catalogs, matrices and diagrams

Goal: pick the right application views.

- Catalogs: Application Portfolio, Interface.
- Matrices: Application/Organization, Role/Application, Application/Function, Application Interaction.
- Diagrams: Application Communication, Application and User Location, Application Use-Case, Enterprise Manageability, Process/Application Realization, Software Engineering, Application Migration, Software Distribution.

Gotchas:
- Interface catalogs rot fastest; link them to the integration platform if possible.
- Show direction and protocol on interaction diagrams.

Verify: every interface in the diagram appears in the Interface catalog.
