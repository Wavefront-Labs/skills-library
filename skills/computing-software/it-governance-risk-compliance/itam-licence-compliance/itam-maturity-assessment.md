---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.itam-maturity-assessment
name: itam-maturity-assessment
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [itam-maturity-assessment, itam-programme-governance, maturity model, iso 19770-1 tiers, roadmap, gap analysis, itam-licence-compliance]
level: advanced
status: draft
description: "Assess ITAM maturity against ISO 19770-1 tiers and build a phased improvement roadmap with quick wins."
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

# ITAM maturity assessment and roadmap

Goal: choose what to fix first based on evidence, not ambition.

Method:
- ISO/IEC 19770-1 defines tiers: trustworthy data (tier 1), practical management (2), operational integration (3), full ISO/IEC 19770-1 conformance (4); confirm current tier wording in the standard.
- Score each process area 0-4 via interviews plus sampled evidence (e.g. 30 assets traced from PO to disposal).
- Rank gaps by risk (audit exposure, spend) times effort.
- Roadmap in 90-day increments: first tier 1 (reliable inventory and entitlement for top 5 vendors).

Gotchas:
- Self-assessment without sampled evidence overstates maturity.
- Tools do not raise maturity unless process and ownership exist.

Verify: the roadmap lists owner, date and a measurable exit criterion per item.
