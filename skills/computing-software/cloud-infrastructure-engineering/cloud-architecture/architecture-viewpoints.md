---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-viewpoints
name: architecture-viewpoints
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-principles, togaf, architecture-viewpoints, content-metamodel, iso-42010, archimate, catalogs-matrices-diagrams, views]
level: practitioner
status: draft
description: "Choose architecture viewpoints for each stakeholder concern (ISO/IEC/IEEE 42010, TOGAF catalogs/matrices/diagrams, ArchiMate) and keep views consistent with one metamodel."
sources: ["https://pubs.opengroup.org/togaf-standard/architecture-content/chap01.html", "https://www.iso.org/standard/74393.html", "https://pubs.opengroup.org/architecture/archimate3-doc/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Content metamodel with viewpoints and views

## Concepts (ISO/IEC/IEEE 42010)
- **Stakeholder** has **concerns**; a **viewpoint** defines conventions (model kinds, notations)
  for framing certain concerns; a **view** is the actual artefact for one system.
- TOGAF content framework expresses views as **catalogs** (lists), **matrices** (relationships) and
  **diagrams**, all drawn from one **content metamodel** (actors, capabilities, applications, data
  entities, technology components, and their relationships).

## Steps
1. From the stakeholder map, list concerns per stakeholder (cost, security, availability,
   integration impact, delivery sequence).
2. Pick viewpoints that answer each concern. Common cloud set:
   | Concern | Viewpoint / artefact |
   |---|---|
   | What capabilities change | Capability map heat map |
   | Which apps talk to what | Application communication diagram / interface catalogue |
   | Where data lives | Data entity / location matrix |
   | Runtime topology | Deployment (C4 deployment, ArchiMate technology) diagram |
   | Security boundaries | Trust boundary / network zone diagram |
   | Delivery sequence | Transition architecture roadmap |
3. Fix the metamodel subset you will maintain (element types and relationships) - small enough
   to keep current.
4. Generate views from a model (EA tool or diagrams-as-code) instead of drawing each by hand, so
   renaming an app updates every view.
5. Record viewpoint definitions (purpose, audience, notation, legend) in the architecture repository.

## Gotchas
- One "big picture" diagram for all audiences answers nobody's concern.
- Mixed notations without a legend; always include a key.
- Views drift when not generated from a shared model.

## Verify
- [ ] Every key stakeholder concern maps to at least one view.
- [ ] Each view states its viewpoint, date and owner.
