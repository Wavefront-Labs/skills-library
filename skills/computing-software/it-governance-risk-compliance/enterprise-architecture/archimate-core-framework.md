---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-core-framework
name: archimate-core-framework
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-core-framework, archimate-language-structure, archimate, archimate 3.2, core framework, layers, active structure, behavior, passive structure, aspects, enterprise-architecture]
level: intro
status: draft
description: "Read the ArchiMate core framework grid of Business, Application and Technology layers against active structure, behaviour and passive structure aspects."
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

# ArchiMate core framework: layers and aspects

Goal: place any element in the framework.

- Layers: Business, Application, Technology (with the physical elements as an extension of Technology).
- Aspects: active structure (who or what acts), behaviour (what is done), passive structure (what is acted on).
- Full framework adds Strategy, Motivation, and Implementation and Migration as extensions.
- Layers connect through serving and realization relationships.

Gotchas:
- Aspects are not layers; do not draw them as boxes.
- ArchiMate is a modelling language, not a method; pair with TOGAF.

Verify: you can classify ten given elements by layer and aspect.
