---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.entitlement-data-collection
name: entitlement-data-collection
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [entitlement-data-collection, entitlement-schema-iso-19770-3, entitlement collection, vlsc, reseller report, proof of entitlement, contract repository, itam-licence-compliance]
level: practitioner
status: draft
description: "Gather entitlement data from vendor portals, resellers and contracts, normalise it and prove it for audit."
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

# Collecting entitlement data from vendors

Goal: complete and provable licence entitlement.

Method:
- Sources: contracts, purchase orders, reseller licence statements, vendor portals (Microsoft 365 admin center and Volume Licensing Service Center/Admin portal, Oracle Support, IBM Passport Advantage/ILMT) and invoices.
- Normalise product names to a catalogue; map to metrics.
- Attach evidence and record who validated and when.
- Ask the reseller for an annual entitlement statement.
- Resolve conflicts: contract prevails over portal.

Gotchas:
- M&A acquired contracts are often missing; check legal archives.
- Pre-2010 perpetual licences without proof are risky; keep original media or invoices.

Verify: top 10 vendors have 100% entitlements with evidence.
