---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.tco-and-chargeback
name: tco-and-chargeback
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [tco-and-chargeback, asset-financial-management, tco, showback, chargeback, cost allocation, unit cost, itam-licence-compliance]
level: advanced
status: draft
description: "Calculate total cost of ownership for IT assets and allocate cost by showback or chargeback to business units."
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

# TCO, showback and chargeback

Goal: make consumption visible and fairly charged.

Method:
- TCO components: acquisition, licences, support, power/space, admin labour, disposal, minus residual value.
- Allocation drivers: seat count, device count, CPU hours, storage GB.
- Showback first (report only), chargeback after cost data is trusted and accepted.
- Publish unit cost per service (e.g. cost per managed laptop per month).

Gotchas:
- Unfair allocation destroys trust; agree drivers with business owners.
- Shared platforms need explicit overhead rules.

Verify: allocated totals equal the underlying spend for the period.
