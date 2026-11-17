---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.itam-policy-and-charter
name: itam-policy-and-charter
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [itam-policy-and-charter, itam-programme-governance, asset policy, charter, iso 19770-1, governance, itam-licence-compliance]
level: intro
status: draft
description: "Write an ITAM policy and charter that fix scope, authority, owners and objectives so asset data is trusted."
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

# ITAM policy, charter and scope

Goal: establish a mandate so ITAM can enforce process across procurement, IT and finance.

Method:
- Define scope: hardware, software, cloud/SaaS, mobile, OT/IoT, virtual assets; state what is excluded and why.
- Name an executive sponsor, an ITAM owner and data owners per asset class.
- State objectives as measurable targets (inventory accuracy %, licence position coverage, audit readiness days).
- Mandate that no purchase or deployment bypasses the asset record (no PO without asset ID plan).
- Review annually and after any audit or merger.

Gotchas:
- A policy without procurement and finance sign-off is ignored.
- Scope creep into every spreadsheet dilutes effort; start with highest-risk vendors.

Verify: sponsor signature exists, scope list is published, and one control (e.g. PO gate) is actually enforced.
