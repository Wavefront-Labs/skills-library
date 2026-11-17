---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.inventory-reconciliation
name: inventory-reconciliation
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [inventory-reconciliation, asset-inventory-discovery, reconciliation, data quality, identification rules, golden record, dedupe, itam-licence-compliance]
level: advanced
status: draft
description: "Reconcile discovery, finance and CMDB sources with match keys, tolerance rules and a data quality scorecard."
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

# Inventory reconciliation and data quality

Goal: a single trusted record per asset.

Method:
1. Choose match keys in order: serial number, then MAC, then hostname plus FQDN, then asset tag.
2. Define source precedence per attribute (finance for cost, discovery for OS, HR for owner).
3. Auto-merge on exact key; queue near matches for manual review.
4. Score quality: completeness (required fields filled), accuracy (sample audits), timeliness (last seen under 30 days).
5. Publish the scorecard monthly with owners for the worst classes.

Gotchas:
- VMs cloned from a template can share MACs/serials; add UUID.
- Hostname reuse after rebuilds creates false merges.

Verify: physical audit of 50 random assets scores at least 95% accurate.
