---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-specialization-profiles
name: archimate-specialization-profiles
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-specialization-profiles, archimate-customisation, specialization, profile, language customization, custom element type, domain specific, attributes, enterprise-architecture]
level: advanced
status: draft
description: "Extend the language by defining specializations of elements and relationships with profiles and attributes."
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

# Specializations and profiles

Goal: add domain terms while staying conformant.

- A specialization narrows an element type with a profile name (for example Application Component specialised as Microservice).
- Profiles may carry an icon and shape tweak; keep the underlying type.
- Provide a definition and usage guideline per profile.
- Use in tools through profile or specialization features (Archi supports specializations).

Gotchas:
- Do not invent new core types; use specialization to stay exchangeable.

Verify: models with profiles still validate against the standard.
