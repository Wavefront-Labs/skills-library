---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.effective-licence-position
name: effective-licence-position
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [effective-licence-position, sam-process-and-licence-position, elp, effective licence position, reconciliation, compliance position, over licensed, under licensed, itam-licence-compliance]
level: practitioner
status: draft
description: "Compute an effective licence position by reconciling normalised installs and usage to entitlements per metric."
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

# Effective licence position (ELP)

Goal: show surplus or shortfall per product and its cost.

Method:
1. Normalise discovered software to products/editions.
2. Convert usage to the licence metric (users, devices, processor cores with core factor, PVU).
3. Apply rights: downgrade, virtualisation, multiple-use, secondary copy.
4. Subtract from entitlements, allowing for term and maintenance.
5. Price shortfall at list less expected discount to present exposure; present surplus as savings opportunity.
6. Record assumptions and unresolved questions per line.

Gotchas:
- A product-level position hides edition mismatches.
- Reporting without assumptions is not defensible to a vendor.

Verify: have a colleague recompute one vendor from raw data and compare.
