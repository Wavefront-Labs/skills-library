---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.physical-audit-and-stocktake
name: physical-audit-and-stocktake
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [physical-audit-and-stocktake, asset-inventory-discovery, stocktake, physical audit, cycle count, write off, barcode scanning, itam-licence-compliance]
level: practitioner
status: draft
description: "Run sample-based or full physical stocktakes with barcode scanning, exception handling and write-off approval."
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

# Physical audit and stocktake

Goal: prove records match reality and fix drift.

Method:
- Plan: choose full or cycle counts (e.g. quarterly by location); freeze moves during count.
- Scan each asset tag with a handheld or phone app; log location and condition.
- Reconcile: missing (in records, not found), surplus (found, not recorded), mismatched location.
- Investigate missing assets for 30 days; then request finance-approved write-off with police report for theft.
- Report accuracy % and root causes (e.g. shadow IT, unlogged moves).

Gotchas:
- Remote workers: use self-attestation with photo or MDM check-in.
- Do not just edit the record to match; fix the process cause.

Verify: variance trend improves each cycle.
