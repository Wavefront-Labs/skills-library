---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.standards-and-catalogue
name: standards-and-catalogue
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [standards-and-catalogue, hardware-procurement-and-sourcing, standard build, catalogue, hardware standards, request fulfilment, itam-licence-compliance]
level: practitioner
status: draft
description: "Define standard hardware models and a request catalogue to cut variety, support cost and licence sprawl."
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

# Hardware standards and catalogue

Goal: fewer models, cheaper support, faster provisioning.

Method:
- Group personas (office, developer, field, executive) and select 1-2 models each.
- Set refresh age and specification floor (RAM, storage, TPM 2.0, secure boot).
- Publish a catalogue with price, lead time and approval route; non-catalogue requests need exception approval.
- Review quarterly with supplier roadmap and end-of-sale notices.

Gotchas:
- Too tight a standard produces shadow purchases.
- Model transitions leave mixed fleets; track driver and image support.

Verify: share of purchases from catalogue exceeds 90%.
