---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.gap-analysis-capability-based
name: gap-analysis-capability-based
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [gap-analysis-capability-based, gap-analysis-technique, consolidated gaps, cross domain gap, capability gap, gap register, gap prioritisation, enterprise-architecture]
level: practitioner
status: draft
description: "Extend gap analysis across business, data, application and technology and consolidate into a single gap list."
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

# Gap analysis across domains and capabilities

Goal: a consolidated gap register.

- Run per domain then link gaps across domains (a new business service implies application and data gaps).
- Record each gap with ID, description, domain, impact, owner and proposed resolution.
- Rate severity and effort for prioritisation.
- Feed the register to Phase E for grouping.

Gotchas:
- Linking cross-domain gaps avoids duplicate work packages.
- Keep IDs stable.

Verify: each gap traces to a work package or an accepted-risk entry.
