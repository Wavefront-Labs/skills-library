---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.time-model-assessment
name: time-model-assessment
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [time-model-assessment, application-portfolio-rationalisation, time model, tolerate invest migrate eliminate, application portfolio, rationalisation, apm, application disposition, gartner time, enterprise-architecture]
level: practitioner
status: draft
description: "Classify applications by business value and technical fit into Tolerate, Invest, Migrate or Eliminate."
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

# TIME model: Tolerate, Invest, Migrate, Eliminate

Goal: decide each application's fate consistently.

1. Score business value (strategic fit, usage, criticality).
2. Score technical quality (supportability, security, cost, architecture fit).
3. Plot: high value/high quality = Invest; high value/low quality = Migrate; low value/high quality = Tolerate; low value/low quality = Eliminate.
4. Validate with owners; record rationale.
5. Feed into roadmap and budget.

Gotchas:
- Scores must use agreed criteria and evidence.
- Add extra categories (such as Reengineer or Consolidate) only if used.

Verify: every application in scope has a TIME category and owner.
