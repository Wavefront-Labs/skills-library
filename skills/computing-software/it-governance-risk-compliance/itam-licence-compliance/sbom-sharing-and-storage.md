---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.sbom-sharing-and-storage
name: sbom-sharing-and-storage
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [sbom-sharing-and-storage, sbom-distribution-and-integrity, sbom sharing, sbom repository, nda, discovery, sbom exchange, access control, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Decide how to share SBOMs with customers: public URLs, portals under NDA, registries and discovery options, using the NTIA sharing guidance as a start."
sources:
  - https://www.ntia.gov/page/software-bill-materials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SBOM sharing, access control and repositories

Goal: right audience gets the right level of detail.

Method:
- Read the NTIA "Sharing and Exchanging SBOMs" document (linked from the NTIA SBOM page): it describes how SBOM data can flow down the supply chain and offers a small set of discovery and access options.
- Choose a model: public SBOM for open-source products, authenticated portal for customers, or regulated submission.
- Provide a stable location per product and version, and link it from release notes.
- Version SBOMs and keep history for supported releases.
- Redact sensitive internal component names if necessary (tradeoff with completeness).
- Keep an internal central store as the source of truth.
- Use a machine-readable format; the NTIA survey of formats highlights SPDX, CycloneDX and SWID.

Gotchas:
- SBOM leakage can aid attackers; control access but avoid security through obscurity.
- Customer SBOM requests may be bound by an NDA; check before sharing.

Verify: any shipped version has a retrievable SBOM.

## Checked

2026-11-09. Read the NTIA Software Bill of Materials page in full. It confirms the Sharing and Exchanging SBOMs document (discovery and access options), the Software Suppliers and Consumers Playbooks, and that SPDX, CycloneDX and SWID are the three highlighted formats. The detail inside the linked NTIA documents was not read. Removed: security.txt and registry discovery conventions, the Dependency-Track and artefact repository examples, and the PDF remark, because no cited page states them. Other former sources (ISO, SPDX, REUSE: blocked or script-only; OpenChain, OSI, GPL FAQ: unrelated to sharing) were dropped.

Method: documentation only; no commands were run.
