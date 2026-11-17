---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-relationship-types
name: archimate-relationship-types
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-relationship-types, archimate-relationships-topic, composition, aggregation, assignment, realization, serving, access, influence, association, triggering, flow, specialization, relationship types, enterprise-architecture]
level: practitioner
status: draft
description: "Choose composition, aggregation, assignment, realization, serving, access, influence, association, triggering, flow and specialization correctly."
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

# Relationship types: structural, dependency, dynamic and other

Goal: pick the right relationship.

- Structural: composition (part of, existence dependent), aggregation (groups), assignment (allocation of responsibility or performance), realization (implements).
- Dependency: serving (provides functionality), access (read, write, readwrite or unspecified), influence, association (unspecified).
- Dynamic: triggering (temporal or causal), flow (transfer).
- Other: specialization (is a kind of).
- Check the relationship table in the spec for valid pairs.

Gotchas:
- Overusing association hides meaning.
- Triggering is not flow.

Verify: your tool rejects invalid relationships.
