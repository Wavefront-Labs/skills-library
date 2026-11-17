---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.ilmt-operations
name: ilmt-operations
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [ilmt-operations, ibm-licensing, ilmt, ibm license metric tool, bigfix, scan groups, software catalog, quarterly reports, itam-licence-compliance]
level: practitioner
status: draft
description: "Deploy ILMT, keep scan groups healthy, review software catalogue and bundle products, and archive reports on time."
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

# Operating IBM License Metric Tool

Goal: sub-capacity compliance evidence.

Method:
1. Install ILMT server, deploy BigFix agents to all servers with IBM software.
2. Confirm scans complete and software catalogue is current (update the catalogue and KB regularly).
3. Resolve "software with unknown/unresolved product" and assign instances to products and metrics, including bundle/suite relationships (Product bundling, e.g. WebSphere inside Cloud Pak).
4. Generate the Full Software Report (or sub-capacity report) each quarter, sign off and archive.
5. Check agent health daily and fix ones not reporting for over 30 days as per IBM rules (confirm).

Gotchas:
- Missing VM manager connections hide virtual machine to host mapping.
- Auditors will ask for the whole set of quarterly reports.

Verify: no endpoints with outdated scan beyond tolerance.
