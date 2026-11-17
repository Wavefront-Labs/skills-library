---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.telecom-and-line-management
name: telecom-and-line-management
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [telecom-and-line-management, mobile-byod-asset-management, telecom expense management, sim, carrier plan, tem, line inventory, itam-licence-compliance]
level: practitioner
status: draft
description: "Manage mobile lines, SIMs and carrier plans as assets, rightsizing plans and removing unused lines."
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

# Telecom lines, SIMs and carrier contracts

Goal: pay only for lines in use.

Method:
- Inventory each line: number, SIM/eSIM ID, plan, user, device, contract end.
- Pull usage data monthly; flag lines with no use for 90 days.
- Pool data plans and negotiate per-carrier tiers.
- Reconcile invoice to inventory; dispute charges for lines not in inventory.

Gotchas:
- Early termination fees; check term before cancelling.
- International roaming charges need controls (roaming bundles, caps).

Verify: invoice lines without a registered owner trend to zero.
