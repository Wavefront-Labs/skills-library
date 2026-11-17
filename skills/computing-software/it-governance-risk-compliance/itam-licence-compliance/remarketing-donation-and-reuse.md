---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.remarketing-donation-and-reuse
name: remarketing-donation-and-reuse
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [remarketing-donation-and-reuse, itad-and-disposal, remarketing, donation, resale, refurbish, transfer of title, reuse, itam-licence-compliance]
level: intro
status: draft
description: "Reuse, resell or donate retired kit safely: sanitise, remove licences and branding, document transfer of title."
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

# Remarketing, donation and reuse

Goal: recover value without creating liability.

Method:
- Prefer internal redeployment first, then resale via ITAD remarketing, then donation.
- Sanitise first, then remove asset tags, boot passwords, MDM enrolment and corporate software.
- Check that OEM operating system and software licences may transfer; many OEM and volume licences do not (confirm in the licence terms).
- Sign a title-transfer and data-free declaration; remove from insurance and asset register, record proceeds for finance.

Gotchas:
- Donated devices with embedded firmware passwords are bricks.
- Resale of devices with certain firmware features or crypto may face export controls.

Verify: finance reconciles proceeds and records.
