---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.data-management-governance
name: data-management-governance
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [data-management-governance, adm-phase-c-data, master data management, metadata, data governance, data quality, data stewardship, data dictionary, enterprise-architecture]
level: advanced
status: draft
description: "Cover data quality, master data, metadata and governance responsibilities as part of data architecture definition."
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

# Data management and governance considerations

Goal: embed data management disciplines in the architecture.

- Master and reference data: decide registry, consolidation or central hub style per domain.
- Metadata: capture a business glossary and technical catalog; link to ABBs.
- Quality: define rules, thresholds and who fixes defects.
- Governance: stewardship roles, change control on shared definitions.
- Compliance: map entities to retention and privacy obligations.

Gotchas:
- Governance without tooling support is not sustained.
- Do not start with a perfect enterprise model; model by domain and integrate.

Verify: a steward is named for each master data domain.
