---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.technology-architecture-development
name: technology-architecture-development
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [technology-architecture-development, adm-phase-d-technology, phase d, technology architecture, platform services, infrastructure, technology standards, trm, enterprise-architecture]
level: practitioner
status: draft
description: "Define platforms, infrastructure and standards that host the application and data architectures, using technology reference models."
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

# Develop baseline and target technology architecture

Goal: technology building blocks sufficient to host the target applications.

1. Select a technology reference model and viewpoints.
2. List required platform services derived from application and data needs.
3. Describe baseline technology only as needed for gaps.
4. Define target platforms, networks, hosting, and non-functional targets.
5. Define standards, then identify candidate products.

Gotchas:
- Cloud, edge and SaaS need explicit treatment, not an afterthought.
- Resilience and capacity targets must be numeric.

Verify: each application is mapped to a hosting platform in the Application/Technology matrix.
