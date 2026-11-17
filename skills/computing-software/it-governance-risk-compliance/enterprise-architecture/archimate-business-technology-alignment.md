---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-business-technology-alignment
name: archimate-business-technology-alignment
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-business-technology-alignment, archimate-cross-layer, cross layer, layered viewpoint, serving, realization, alignment, technology supports application, enterprise-architecture]
level: practitioner
status: draft
description: "Use serving and realization relationships to connect layers and the layered viewpoint to present the stack."
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

# Alignment between business, application and technology layers

Goal: a full stack story from customer service to infrastructure.

- Technology service serves application components.
- Artifact realizes application component.
- Application service serves business behaviour or actors.
- Application data object realizes business object.
- Present with a Layered viewpoint, then drill into per-layer viewpoints.

Gotchas:
- Skipping layers (business directly to node) is rarely meaningful; add the intermediate elements.

Verify: every serving chain terminates in a business element.
