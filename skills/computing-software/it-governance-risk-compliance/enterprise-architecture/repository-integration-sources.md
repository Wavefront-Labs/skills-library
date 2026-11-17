---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.repository-integration-sources
name: repository-integration-sources
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [repository-integration-sources, repository-management, cmdb integration, ea repository integration, system of record, data synchronization, discovery, api import, enterprise-architecture]
level: advanced
status: draft
description: "Feed the EA repository from the CMDB, cloud inventory, SSO and project systems and decide the system of record per attribute."
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

# Integrate repository with CMDB and other sources

Goal: reduce manual maintenance.

- Define system of record per attribute (for example CMDB for infrastructure, EA tool for capability mapping).
- Use API or file integration with scheduled sync; match on stable keys.
- Log conflicts and resolution rules.
- Respect access control and data classification.

Gotchas:
- Two-way sync loops; choose a direction per attribute.

Verify: a test record changed in the source appears in the repository within the agreed interval.
