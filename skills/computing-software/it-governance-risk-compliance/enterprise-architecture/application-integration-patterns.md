---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.application-integration-patterns
name: application-integration-patterns
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [application-integration-patterns, adm-phase-c-application, integration patterns, api, event driven, messaging, soa, service oriented architecture, batch integration, enterprise-architecture]
level: advanced
status: draft
description: "Select integration styles such as APIs, messaging, events and batch, and apply service-oriented principles to application architecture."
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

# Application integration patterns and service orientation

Goal: choose integration styles deliberately.

- Synchronous request/response APIs for query and command with low latency needs.
- Asynchronous messaging or events to decouple producers and consumers.
- File or batch exchange for bulk or legacy interfaces.
- Apply loose coupling, contract-first design, versioning and idempotency.
- Document the chosen pattern per interface in the Interface catalog.

Gotchas:
- A central bus is not decoupling if every service depends on its schema.
- Define ownership of shared event schemas.

Verify: each interface lists pattern, owner and versioning policy.
