---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.warranty-and-support-contracts
name: warranty-and-support-contracts
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [warranty-and-support-contracts, hardware-procurement-and-sourcing, warranty, maintenance contract, support renewal, end of support, third party maintenance, itam-licence-compliance]
level: practitioner
status: draft
description: "Track warranty and third-party maintenance end dates and decide to renew, replace or self-insure."
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

# Warranty, maintenance and support contracts

Goal: pay for cover only where it is worth it.

Method:
- Store warranty start/end and support tier on each asset; alert 120/60/30 days ahead.
- Decision matrix per class: critical servers get vendor support; commodity laptops self-insure with spares.
- Evaluate third-party maintenance for end-of-life servers and network gear versus vendor extended support (confirm firmware access terms).
- Consolidate renewals to one co-terminus date per vendor when possible.

Gotchas:
- Support on retired hardware is a common wasted spend; reconcile contracts against live assets.
- Resellers may drop support upon contract migration.

Verify: every maintenance line item maps to an active asset.
