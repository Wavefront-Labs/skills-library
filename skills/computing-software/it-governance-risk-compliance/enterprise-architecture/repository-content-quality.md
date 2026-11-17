---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.repository-content-quality
name: repository-content-quality
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [repository-content-quality, repository-management, repository management, model quality, naming conventions, content ownership, lifecycle states, data quality, stale content, enterprise-architecture]
level: practitioner
status: draft
description: "Define ownership, naming conventions, lifecycle states and quality checks so the repository stays trustworthy."
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

# Repository content governance and quality

Goal: a repository people use and trust.

- Assign an owner per domain and per element type.
- Naming conventions and IDs; avoid duplicates.
- Lifecycle states: draft, proposed, approved, retired.
- Quality checks: orphans, missing owners, invalid relationships, stale review dates.
- Run automated checks (tool scripts or queries) monthly.

Gotchas:
- Over-collecting data nobody maintains; collect only what drives decisions.

Verify: quality report is published and shows trends.
