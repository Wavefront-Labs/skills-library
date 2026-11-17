---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.cmdb-vs-asset-register
name: cmdb-vs-asset-register
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [cmdb-vs-asset-register, configuration-management-cmdb, cmdb, asset register, configuration item, itil, ci vs asset, itam-licence-compliance]
level: intro
status: draft
description: "Separate the financial asset register from the CMDB of configuration items and integrate them by shared keys."
sources:
  - https://www.iso.org/standard/68291.html
  - https://spdx.github.io/spdx-spec/
  - https://cyclonedx.org/specification/overview/
  - https://www.ntia.gov/page/software-bill-materials
  - https://openchainproject.org/
  - https://reuse.software/spec/
  - https://opensource.org/licenses
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CMDB versus asset register

Goal: avoid duplicate, conflicting records.

Differences:
- Asset register: financial and contractual lifecycle (cost, owner, warranty, depreciation).
- CMDB: configuration items and their relationships for service impact (dependencies, versions).
- Not every asset is a CI (a spare keyboard) and not every CI is an asset (a logical service or application instance).

Method:
- Pick a shared unique key (asset ID or serial) and one system of record per attribute.
- Sync via integration, not re-keying.
- Define CI classes (server, application, database, network device) and mandatory attributes.

Gotchas:
- A CMDB with no governance decays within months.
- Importing everything raises the maintenance burden; model what you will use for change and incident decisions.

Verify: a change risk query returns correct dependents for a sampled server.
