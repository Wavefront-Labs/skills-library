---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-business-active-behavior
name: archimate-business-active-behavior
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-business-active-behavior, archimate-business-layer, business actor, business role, business collaboration, business process, business function, business service, business interface, business event, business interaction, enterprise-architecture]
level: practitioner
status: draft
description: "Model business active structure and behaviour: actor, role, collaboration, interface, process, function, interaction, event and service."
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

# Business actors, roles, collaborations, processes, functions and services

Goal: correct business layer modelling.

- Actor performs roles via assignment; role is assigned to process or function.
- Process is a sequence with a defined start and end; function groups behaviour by competence; interaction is shared by collaborations.
- Business service is the externally visible behaviour; interface is the channel.
- Event triggers or is raised by behaviour.
- Use triggering and flow between processes; serving from service to consumer.

Gotchas:
- Do not model organisation units as roles.
- Processes are not capabilities.

Verify: each process has an assigned role and appears in a service realization chain.
