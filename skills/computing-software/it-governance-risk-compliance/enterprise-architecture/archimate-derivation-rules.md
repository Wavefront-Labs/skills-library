---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-derivation-rules
name: archimate-derivation-rules
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-derivation-rules, archimate-relationships-topic, derivation rules, derived relationship, junction, and junction, or junction, relationship chain, valid derivation, potential derivation, enterprise-architecture]
level: advanced
status: draft
description: "Derive relationships through structural and dependency chains, and use and/or junctions to combine same-type relationships."
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

# Relationship derivation and junctions

Goal: reason about indirect relationships safely.

- Chains of structural relationships (composition, aggregation, assignment, realization) derive a relationship of the weakest type in the chain.
- Dependency relationships can derive from structural chains followed by a dependency.
- A junction (and/or) joins relationships of the same type only, except for association.
- The spec distinguishes valid derivations from potential ones; confirm the specific rules in the current relationship tables.

Gotchas:
- Do not derive a relationship that was not intended just because it is allowed.
- Tools differ in derivation support.

Verify: any derived relation you show passes the spec derivation rule.
