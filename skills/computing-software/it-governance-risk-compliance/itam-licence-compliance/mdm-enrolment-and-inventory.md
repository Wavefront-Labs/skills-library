---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.mdm-enrolment-and-inventory
name: mdm-enrolment-and-inventory
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [mdm-enrolment-and-inventory, mobile-byod-asset-management, mdm, uem, intune, jamf, imei, enrolment, apple business manager, android enterprise, itam-licence-compliance]
level: practitioner
status: draft
description: "Enrol corporate and BYOD devices with MDM, capture IMEI and carrier data, and sync inventory to the asset register."
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

# MDM enrolment and mobile inventory

Goal: complete, current mobile inventory.

Method:
- Corporate devices: zero-touch enrolment (Apple Business Manager automated device enrolment, Android Enterprise zero-touch, Windows Autopilot).
- BYOD: user enrolment or app-level management only, with a clear privacy statement.
- Capture IMEI, serial, phone number, carrier plan, OS version.
- Sync MDM inventory to the ITAM register by serial each day.
- Compliance policy: block corporate access for unenrolled or unsupported OS devices.

Gotchas:
- Number porting and SIM swaps change the link between device and line; track lines separately.
- Personal devices cannot be wiped fully; selective wipe only.

Verify: MDM count equals ITAM mobile count within 2%.
