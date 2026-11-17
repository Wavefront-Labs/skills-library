---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.adobe-vip-etla
name: adobe-vip-etla
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [adobe-vip-etla, adobe-licensing, adobe vip, etla, creative cloud, named user licence, shared device licence, admin console, itam-licence-compliance]
level: practitioner
status: draft
description: "Understand Adobe VIP, ETLA and named-user versus shared device licensing and manage assignment through Admin Console."
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

# Adobe VIP and ETLA models

Goal: pay for the Adobe seats actually used.

- VIP: reseller-based, flexible, annual or multi-year, with discount tiers.
- ETLA: enterprise-wide term agreement with custom pricing, anniversary true-up.
- Named user licence: tied to a person; shared device licence: for labs, tied to a device.
- Adobe Admin Console: assign products to users, set auto-deprovision on inactivity, sync from Entra ID/Okta.

Method: reclaim seats from users inactive for 60-90 days, use product profiles by role, compare All Apps versus single-app plans.

Gotchas:
- Mid-term reductions are usually not allowed; reduce at renewal.
- Personal Adobe IDs used for company work bypass management; require federated IDs.

Verify: admin console seat counts match contract.
