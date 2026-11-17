---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.ntia-minimum-elements
name: ntia-minimum-elements
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [ntia-minimum-elements, sbom-minimum-elements, ntia, minimum elements, supplier name, component name, version, unique identifiers, dependency relationship, author, timestamp, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Provide the seven NTIA baseline data fields, automation support and practices that define a minimum viable SBOM."
sources:
  - https://www.ntia.gov/sites/default/files/publications/sbom_minimum_elements_report_0.pdf
  - https://www.ntia.gov/page/software-bill-materials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NTIA minimum elements

Goal: meet the US baseline.

NTIA (July 2021) data fields: Supplier Name, Component Name, Version of the Component, Other Unique Identifiers (purl, CPE), Dependency Relationship, Author of SBOM Data, Timestamp.
Automation support: machine-readable formats (SPDX, CycloneDX, SWID).
Practices and processes: frequency (new SBOM with each new build/release), depth (all primary components with their transitive dependencies), known unknowns (explicitly identify an incomplete dependency graph), distribution and delivery, access control, accommodation of mistakes.

Method: map your generator's output to each field; fill gaps (supplier is commonly missing) with enrichment.

Gotchas:
- This is the 2021 NTIA baseline; check CISA for any newer minimum-elements guidance (the CISA page could not be read when this skill was checked).

Verify: map each of the seven data fields to your SBOM output; sbomqs reports NTIA compliance.

## Checked

2026-11-02. Checked against the NTIA Minimum Elements report (12 July 2021): the seven data fields, automation support formats (SPDX, CycloneDX, SWID), the practices and processes list (frequency, depth, known unknowns, distribution and delivery, access control, accommodation of mistakes) and CPE / SWID / PURL as example identifiers; and the sbomqs README (NTIA validation). Removed: the 2025 CISA draft claim (cisa.gov returned 403), the UTC timestamp rule and the conformance-checker tool name.

Method: documentation only; no commands were run.
