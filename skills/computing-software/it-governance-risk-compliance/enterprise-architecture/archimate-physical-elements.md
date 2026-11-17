---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-physical-elements
name: archimate-physical-elements
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-physical-elements, archimate-technology-layer, equipment, facility, distribution network, material, physical elements, iot, manufacturing, enterprise-architecture]
level: advanced
status: draft
description: "Model physical-world entities such as equipment, facilities, networks for material and the materials themselves for logistics or IoT contexts."
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

# Physical elements: equipment, facility, distribution network, material

Goal: bring physical assets into the architecture model.

- Equipment: physical machines or tools; facility: a physical structure such as a factory; distribution network: physical network for material or energy; material: physical matter or energy.
- Physical elements specialise Node (equipment, facility) and can host technology or be hosted by locations.
- Use realization from material to an artifact or from artifact to material in systems that produce physical things.

Gotchas:
- Use only when relevant; default to the technology layer.

Verify: the physical view links each device to a facility and location.
