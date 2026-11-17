---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.adr-process-governance
name: adr-process-governance
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [adr-process-governance, architecture-decision-records, decision process, adr review, decision log, architecture significant decision, governance linkage, architecturally significant, enterprise-architecture]
level: practitioner
status: draft
description: "Run a lightweight decision process: when an ADR is required, who reviews, and how ADRs connect to principles and the repository."
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

# ADR process, review and linking to governance

Goal: decisions are made visibly and quickly.

- Trigger: architecturally significant decisions (hard to reverse, cross-team, affecting quality attributes).
- Draft in a pull request; reviewers include affected teams and an architect; time-box discussion.
- Link the ADR to principles, requirements and affected components.
- Index ADRs in a list and surface in the repository; for enterprise-level, store in the Governance Log.

Gotchas:
- Skipping ADRs for "obvious" decisions loses the rationale.

Verify: ADR index is complete and each accepted ADR has a decision date and approver.
