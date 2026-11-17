---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.requirements-capture-traceability
name: requirements-capture-traceability
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [requirements-capture-traceability, requirements-management, requirements management, requirements traceability, architecture requirements specification, requirement repository, requirement status, enterprise-architecture]
level: practitioner
status: draft
description: "Keep a requirements repository with source, priority, status and traceability to architecture elements across ADM phases."
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

# Capture and trace architecture requirements

Goal: requirements are identified, stored and linked as the ADM progresses.

- Record each requirement with ID, source stakeholder, type (functional, NFR, constraint), priority and status.
- Link requirements to concerns, viewpoints, ABBs and work packages.
- Re-baseline after each phase when requirements change.
- Feed new or changed requirements to the phase that must react.

Gotchas:
- Keep requirements atomic and testable.
- Do not delete requirements; supersede them to preserve history.

Verify: each ABB traces to one or more requirements and vice versa.
