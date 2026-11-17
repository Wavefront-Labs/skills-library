---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.capitalisation-and-depreciation
name: capitalisation-and-depreciation
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [capitalisation-and-depreciation, asset-financial-management, capex, depreciation, capitalisation, useful life, book value, straight line, itam-licence-compliance]
level: practitioner
status: draft
description: "Apply capitalisation thresholds and depreciation schedules to hardware and capitalised software and keep records aligned."
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

# Capitalisation and depreciation of IT assets

Goal: ITAM and finance agree on what an asset is worth.

Method:
- Set a capitalisation threshold (e.g. unit cost above a policy limit) and group low-cost items as pools.
- Typical useful lives: laptops 3-4 years, servers 4-5, network 5; confirm with your accountants and jurisdiction.
- Straight-line depreciation: (cost - residual) / life; record monthly.
- Capitalised internal-use software has its own rules (confirm with ASC 350-40 / IAS 38).
- Feed disposal events to finance for gain/loss on disposal.

Gotchas:
- Assets retired early need an impairment or accelerated write-off.
- Tax and book lives may differ.

Verify: fixed asset ledger reconciles to the ITAM register quarterly.
