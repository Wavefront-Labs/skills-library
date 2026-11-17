---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.sap-usmm-and-law
name: sap-usmm-and-law
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [sap-usmm-and-law, sap-licensing, usmm, law, license administration workbench, slicense, sap measurement, sap audit, itam-licence-compliance]
level: sme
status: draft
description: "Run USMM and consolidate with LAW to produce SAP licence measurement, reconcile and submit to SAP."
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

# SAP USMM and LAW measurement

Goal: reliable annual measurement.

Method:
1. In each productive system run transaction USMM (system measurement) to get user counts per type and engine measurements.
2. For multi-system landscapes, use LAW (License Administration Workbench) to consolidate users across systems so each user is counted once at the highest type.
3. Review user classification; fix before the measurement is final.
4. Run SLICENSE to install new licence keys and check temporary keys.
5. Retain measurement results with the audit trail.

Gotchas:
- Duplicate users (different IDs for one person) inflate counts; use LAW's consolidation by user master matching.
- Run measurement on production only, per instructions of SAP.

Verify: LAW consolidated result reconciled to contract quantities.
