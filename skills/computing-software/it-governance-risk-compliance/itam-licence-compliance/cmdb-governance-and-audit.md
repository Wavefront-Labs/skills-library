---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.cmdb-governance-and-audit
name: cmdb-governance-and-audit
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [cmdb-governance-and-audit, configuration-management-cmdb, cmdb health, attestation, stale ci, cmdb audit, data owner, itam-licence-compliance]
level: advanced
status: draft
description: "Apply CMDB governance with data owners, attestation, health metrics and retire-stale-CI automation."
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

# CMDB governance and integrity audits

Goal: keep CMDB trustworthy enough for change decisions.

Method:
- Assign data owners per CI class; run quarterly attestation for critical services.
- Health metrics: completeness, correctness, compliance (required relationships exist), staleness (last discovered).
- Automate: CIs not seen in N days move to Retired after notification.
- Integrate change management: closing a change requires CI update or an exemption.

Gotchas:
- Do not measure only record count; measure usefulness (percent of incidents using CMDB data).
- Manual overrides conflicting with discovery cause flapping; lock fields by source.

Verify: audit sample of 25 critical CIs, target at least 95% correct.
