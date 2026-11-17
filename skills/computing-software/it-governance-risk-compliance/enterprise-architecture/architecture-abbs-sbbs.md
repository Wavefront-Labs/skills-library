---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.architecture-abbs-sbbs
name: architecture-abbs-sbbs
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [architecture-abbs-sbbs, togaf-core-concepts, abb, sbb, building blocks, architecture building block, solution building block, reuse, enterprise-architecture]
level: practitioner
status: draft
description: "Define reusable ABBs (what is needed) and SBBs (how it is met), and trace them between phases and the repository."
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

# Architecture Building Blocks and Solution Building Blocks

Goal: describe capability as reusable building blocks at the right abstraction.

- ABB: a requirement-level capability or service, product independent. Capture name, functionality, interfaces and the standards it must meet.
- SBB: a specific product, component or configuration that implements one or more ABBs.
- Early in the ADM you define ABBs; later phases (E and F) select SBBs and group them into work packages.
- Store both in the Architecture Repository with relationships so reuse can be found.

Gotchas:
- Naming a vendor product in an ABB turns it into an SBB and hides alternatives.
- Granularity too fine makes the catalogue unmanageable; aim for blocks a team can own.

Verify: every SBB traces to at least one ABB and every ABB has a candidate or chosen SBB by Phase E.
