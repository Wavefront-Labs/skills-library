---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.entitlement-record-structure
name: entitlement-record-structure
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [entitlement-record-structure, entitlement-schema-iso-19770-3, entitlement schema, iso 19770-3, licence metric, entitlement record, rights, restrictions, itam-licence-compliance]
level: advanced
status: draft
description: "Model licence entitlements with metrics, quantities, validity, rights and restrictions as in ISO/IEC 19770-3."
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

# Entitlement record structure

Goal: a machine-readable record of what you may use.

Concepts in the standard: an entitlement ties a licensor, licensee, product, licence metric (user, device, core, processor), quantity, validity period, and rights/restrictions (installation location, virtualisation, downgrade, transfer).
Record each purchase line as: contract ID, product and edition, metric, quantity, term (perpetual/subscription/dates), covered entities, support/maintenance end, source document.

Method:
- Store the entitlement separately from the installation; entitlements are consumed by installations during reconciliation.
- Keep attachments (contract, order form, proof of purchase).
- Capture upgrade, downgrade and transfer rights explicitly.

Gotchas:
- Bundles must be decomposed to constituent entitlements.
- Confirm exact element names against the published schema.

Verify: each record links to a source document.
