---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.adobe-reduction-and-audit-risk
name: adobe-reduction-and-audit-risk
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [adobe-reduction-and-audit-risk, adobe-licensing, adobe audit, perpetual versions, cs6, acrobat, unlicensed installs, creative suite, itam-licence-compliance]
level: advanced
status: draft
description: "Review Adobe installs vs entitlements, remove stale versions and unlicensed perpetual copies and prepare for audit."
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

# Adobe usage review and audit risk

Goal: close the common Adobe compliance gaps.

Method:
- Discover Acrobat, Creative Cloud and legacy Creative Suite installs; Acrobat Reader is free, Acrobat Standard/Pro need licences.
- Distinguish perpetual (e.g. old Acrobat Pro 2017) from subscription; perpetual need proof of purchase.
- Remove old CS versions or document licence proof; Adobe discontinued activation for some versions, confirm.
- Check cloned images that carry serial numbers.
- Compare account activity: users with product assigned but no last-launch.

Gotchas:
- Extension of a trial or reuse of a serial across users is a violation.
- Mixed use of personal and enterprise accounts.

Verify: install count per product is at or below entitlements.
