---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.adm-inputs-outputs-flow
name: adm-inputs-outputs-flow
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [adm-inputs-outputs-flow, adm-overview, request for architecture work, statement of architecture work, architecture definition document, architecture requirements specification, architecture roadmap, architecture contract, enterprise-architecture]
level: practitioner
status: draft
description: "Trace the key deliverables between ADM phases: Request for Architecture Work, Statement of Architecture Work, ADD, Roadmap, Contract."
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

# ADM inputs, outputs and deliverable flow

Goal: know which deliverable is created where and consumed where.

- Request for Architecture Work (from the sponsor, before A) triggers a cycle.
- Statement of Architecture Work (A) is the agreement on scope, approach and schedule.
- Architecture Definition Document and Architecture Requirements Specification grow through B, C and D.
- Architecture Roadmap and Implementation and Migration Plan come from E and F.
- Architecture Contract and Compliance Assessment belong to G.
- Change Requests and updated requirements come from H.

Gotchas:
- Treat the ADD as one living document with baseline and target per domain, not four disconnected files.
- Output names vary between 9.2 and 10; map them once in your tailoring.

Verify: a matrix lists each deliverable, owner phase and approver.
