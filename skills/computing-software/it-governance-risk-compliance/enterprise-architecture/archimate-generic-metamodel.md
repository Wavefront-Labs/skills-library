---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-generic-metamodel
name: archimate-generic-metamodel
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-generic-metamodel, archimate-language-structure, generic metamodel, active structure element, behavior element, passive structure element, service, interface, event, grouping, location, enterprise-architecture]
level: practitioner
status: draft
description: "Use the generic metamodel concepts such as internal and external active structure, internal behaviour, services, events, plus grouping and location."
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

# Generic metamodel: elements, relationships, layers of abstraction

Goal: apply the same pattern in each layer.

- Active structure: internal active structure element (actor, component, node) performs behaviour; interface exposes services externally.
- Behaviour: internal behaviour elements (process, function, interaction); service exposes behaviour; event triggers or results.
- Passive structure: object that is accessed.
- Composite: grouping aggregates elements; location indicates place; junction combines relationships.

Gotchas:
- Interface is the access point, the service is the functionality offered; do not swap.

Verify: each layer in your model follows the pattern of structure, behaviour and service.
