---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-motivation-relationships
name: archimate-motivation-relationships
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-motivation-relationships, archimate-motivation, influence relationship, goal realization, requirements realization, goal contribution, motivation viewpoint, enterprise-architecture]
level: practitioner
status: draft
description: "Use influence with signs, realization and aggregation to build goal and requirement networks."
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

# Motivation relationships: influence, realization and association

Goal: show how goals and requirements relate.

- Influence (dashed, optionally labelled +, ++, -, -- or a value) shows positive or negative contribution; used among motivation elements.
- Realization: requirement realizes goal/outcome; outcome realizes goal.
- Aggregation/composition decompose goals.
- Use Goal Realization, Goal Contribution, Principles, Requirements Realization and Stakeholder viewpoints.

Gotchas:
- Influence is not used between core elements; use serving or flow there.

Verify: conflicting goals are visible with negative influence.
