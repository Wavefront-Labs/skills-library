---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.sap-indirect-and-cloud-licensing
name: sap-indirect-and-cloud-licensing
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [sap-indirect-and-cloud-licensing, sap-licensing, indirect access, digital access, rise with sap, s/4hana, document based pricing, integration, itam-licence-compliance]
level: sme
status: draft
description: "Assess indirect or digital access exposure and understand RISE and S/4HANA cloud licensing consequences."
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

# SAP indirect access and cloud licensing

Goal: identify licensable indirect use.

Method:
- Map interfaces: which third-party systems create or read SAP data through APIs, RFC, IDocs, OData.
- Under the document-based model, certain document types created (e.g. sales orders, invoices) via indirect channels are charged as digital access documents (confirm your contract).
- Compare with named user options for people who use the system via an intermediate app.
- For RISE with SAP and S/4HANA Cloud, the licence model is subscription packages; review the contract metrics and conversion credits.

Gotchas:
- Interface inventories are usually incomplete; involve integration architects.
- Contract conversions can erase previous perpetual rights; seek legal review.

Verify: interface map reviewed by SAP basis and legal.
