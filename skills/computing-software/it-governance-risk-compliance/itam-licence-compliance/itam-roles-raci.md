---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.itam-roles-raci
name: itam-roles-raci
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [itam-roles-raci, itam-programme-governance, raci, asset manager, licence manager, data steward, citam, itam-licence-compliance]
level: practitioner
status: draft
description: "Assign asset manager, licence manager, data steward, procurement and service-desk roles with a RACI per lifecycle step."
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

# ITAM roles and RACI

Goal: make every lifecycle step have exactly one accountable owner.

Method:
1. List lifecycle steps: request, approve, buy, receive, deploy, change, reclaim, dispose.
2. For each, mark Responsible, Accountable (one only), Consulted, Informed across ITAM, procurement, service desk, security, finance and business owner.
3. Typical split: procurement owns PO, ITAM owns record integrity and licence position, service desk owns scan/reclaim at the desk, security owns attestation of wipe, finance owns capitalisation.
4. Document delegations for part-time ITAM teams.

Gotchas:
- Two Accountable roles on one step means no one is.
- Licence manager and software asset manager are not the same as the CMDB owner; keep the data steward explicit.

Verify: pick five recent assets and trace each step to a named person.
