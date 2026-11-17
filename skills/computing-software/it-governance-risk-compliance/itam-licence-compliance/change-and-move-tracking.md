---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.change-and-move-tracking
name: change-and-move-tracking
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [change-and-move-tracking, asset-lifecycle-management, joiner mover leaver, reclaim, reassignment, offboarding, hr feed, itam-licence-compliance]
level: practitioner
status: draft
description: "Track assignment changes, leavers and moves, and reclaim hardware and licences automatically from HR events."
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

# Moves, adds, changes and reclamation

Goal: keep ownership accurate through staff and location churn.

Method:
- Consume the HR feed (joiner, mover, leaver) and open ITAM tasks per event.
- Leaver: recall hardware by day of exit, remove software seats, record condition, return to stock or send to disposal.
- Mover: update cost centre and location; reassess role-based software entitlements.
- Pool devices: scan-based check-out/in with expiry.
- Report unreturned equipment weekly to line managers and finance.

Gotchas:
- Contractors rarely appear in HR feeds; use sponsor-based expiry dates.
- Licences tied to named users stay consumed until removed in the vendor console too.

Verify: leavers from the last 60 days have zero assigned assets or a documented exception.
