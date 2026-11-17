---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.sap-named-user-types
name: sap-named-user-types
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [sap-named-user-types, sap-licensing, sap named user, professional user, limited professional, developer user, engine licence, sap price list, itam-licence-compliance]
level: advanced
status: draft
description: "Classify SAP users into licence types such as Professional and Limited Professional and measure engines separately."
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

# SAP named user types and engines

Goal: assign each SAP user the cheapest valid type.

Method:
- Types vary by contract and year (Professional, Limited Professional, Employee Self-Service, Developer; confirm your contract schedule).
- Assign by business role and transactions executed: heavier users need Professional, occasional/display-only use needs lower types.
- Engines (packages priced by metric such as revenue, orders, headcount) licensed separately.
- Indirect access: using SAP data via third-party systems may require licences (SAP changed policy to document-based pricing in 2018; confirm).

Gotchas:
- Old contracts have legacy types with different definitions.
- Dormant users still count until locked and deleted.

Verify: user role-to-type matrix signed by process owners.
