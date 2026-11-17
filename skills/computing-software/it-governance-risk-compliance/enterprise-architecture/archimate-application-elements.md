---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-application-elements
name: archimate-application-elements
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-application-elements, archimate-application-layer, application component, application collaboration, application interface, application service, application function, application process, data object, enterprise-architecture]
level: practitioner
status: draft
description: "Model application structure and behaviour: component, collaboration, interface, function, process, interaction, event, service, data object."
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

# Application components, collaborations, interfaces, services and data objects

Goal: show applications as encapsulated, modular units.

- Component: a modular, deployable and replaceable part exposing interfaces.
- Application services are exposed behaviours; an application interface is where they are accessed.
- Data object represents data structured for automated processing and is accessed by application behaviour.
- Use serving between applications, flow for data exchange, triggering for control.

Gotchas:
- Do not model a module's internal classes; stay at architecture level.
- A data object is not a database.

Verify: each application service is realized by a component behaviour.
