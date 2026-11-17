---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.sbom-regulatory-drivers
name: sbom-regulatory-drivers
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [sbom-regulatory-drivers, sbom-minimum-elements, eo 14028, cyber resilience act, cra, fda sbom, omb m-22-18, attestation, procurement requirement, itam-licence-compliance]
level: advanced
status: draft
description: "Understand which regulations and contracts require SBOMs, including US EO 14028, EU CRA and FDA premarket guidance."
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

# SBOM regulatory drivers: EO 14028, CRA, FDA

Goal: know when SBOMs are mandatory.

Confirm current status for each:
- US Executive Order 14028 (2021) drove SBOM adoption in federal procurement; OMB memos required secure software attestation (M-22-18, M-23-16) and SBOM requests were left risk-based.
- EU Cyber Resilience Act requires manufacturers of products with digital elements to identify and document components, including drawing up an SBOM in machine-readable form; reporting duties start before full application (confirm dates).
- FDA cyber guidance for medical devices expects an SBOM in premarket submissions.
- Sector and customer contracts increasingly request SPDX or CycloneDX.

Method: build an obligation register mapping regulation, product, due date and deliverable.

Gotchas:
- Legal timelines change; track official sources.
- Customer SBOM requests may be NDA-bound.

Verify: obligation register reviewed by compliance counsel.
