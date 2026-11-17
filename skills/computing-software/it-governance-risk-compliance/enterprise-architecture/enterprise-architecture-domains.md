---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.enterprise-architecture-domains
name: enterprise-architecture-domains
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [enterprise-architecture-domains, togaf-core-concepts, business architecture, data architecture, application architecture, technology architecture, bdat, enterprise scope, enterprise-architecture]
level: intro
status: draft
description: "Separate business, data, application and technology architecture, and scope the enterprise being architected."
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

# Four architecture domains and what an enterprise is

Goal: use the four TOGAF domains consistently and scope the enterprise correctly.

- Business: strategy, governance, organisation, key business processes.
- Data: logical and physical data assets and their management.
- Application: individual systems, their interactions and relation to business processes.
- Technology: hardware, middleware, networks, platforms and standards.
- An enterprise is any collection of organisations with common goals; it may be a business unit, a whole company or a partner network, so define the boundary in the Preliminary phase.

Gotchas:
- Data and application are both Phase C but need separate catalogues and matrices.
- Security and integration cut across all four; treat them as concerns, not a fifth silo.

Verify: each deliverable in your plan is filed under one domain and the enterprise boundary is written down.
