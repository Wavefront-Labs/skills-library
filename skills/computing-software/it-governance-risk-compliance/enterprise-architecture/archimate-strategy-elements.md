---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.archimate-strategy-elements
name: archimate-strategy-elements
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [archimate-strategy-elements, archimate-strategy, resource, capability, value stream, course of action, strategy elements, capability map, value stream map, enterprise-architecture]
level: practitioner
status: draft
description: "Model strategy using resources, capabilities, value streams and courses of action and relate them to core elements."
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

# Resource, capability, value stream and course of action

Goal: represent strategy so it can be traced to implementation.

- Resource: asset owned or controlled; capability: ability of an actor, system or organisation; value stream: sequence of activities creating value for a stakeholder; course of action: approach or plan to achieve a goal.
- Capability is realized by behaviour and resources; value stream stages are realized by capabilities and core behaviour (stages use capabilities, represented with serving).
- Course of action realizes goals or outcomes and is realized by capabilities.

Gotchas:
- Capabilities are stable; courses of action change.

Verify: each course of action links to the capabilities that carry it.
