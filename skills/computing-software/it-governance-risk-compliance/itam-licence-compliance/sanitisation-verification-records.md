---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.sanitisation-verification-records
name: sanitisation-verification-records
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [sanitisation-verification-records, media-sanitisation-nist-800-88, certificate of destruction, verification, sanitisation record, chain of custody, itam-licence-compliance]
level: practitioner
status: draft
description: "Verify sanitisation, keep per-asset records and obtain certificates of destruction that tie to serial numbers."
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

# Sanitisation verification and certificates

Goal: provable evidence for auditors and data-protection regulators.

Method:
- Record per asset: serial, media type, method (clear/purge/destroy), tool and version, operator, date, verification result.
- NIST 800-88 expects verification: sample read-back for Clear, full for high risk where feasible, plus a second-person review.
- Certificate of destruction from a vendor must list serial numbers, date, location, method and witness; reject summary certificates with only counts.
- Store records according to retention policy and link to the asset record.

Gotchas:
- Certificates issued before pickup are a fraud signal.
- A tool log without serial number cannot be matched back.

Verify: pick 20 disposed assets and trace each to a certificate line item.
