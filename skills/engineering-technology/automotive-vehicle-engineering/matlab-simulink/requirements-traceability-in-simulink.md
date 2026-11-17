---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.requirements-traceability-in-simulink
name: requirements-traceability-in-simulink
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [requirements-traceability, requirements, requirements-toolbox, traceability, links, verification]
level: practitioner
status: gated
description: "Link requirements to model elements and tests, keep traceability complete as models change, and produce a coverage-of-requirements report."
sources:
  - "Requirements Toolbox: Import requirements from ReqIF files (https://www.mathworks.com/help/slrequirements/ug/import-requirements-from-reqif-files.html)"
  - "Requirements Toolbox: Implementation status (https://www.mathworks.com/help/slrequirements/ug/review-requirement-implementation-status-metrics-data.html)"
  - "ISO 26262 part 8 and 6 traceability expectations; confirm edition (https://www.iso.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Link requirements to model elements

1. Import or author requirements (ReqIF files, including DOORS exports through the ReqIF mapping) into a requirement set; keep unique stable IDs.
2. Link each requirement to the implementing model element (block, chart state) with `Implement` links and to test cases with `Verify` links.
3. Review the Requirements Perspective or Requirements Editor for unimplemented and unverified requirements (run the analysis first; it is not computed automatically).
4. Keep the links in version control with the model; relink after refactors rather than deleting.
5. Report: requirement coverage = requirements with both implementation and passing verification links; export for assessors.
6. Change impact: when a requirement changes, query its links to find affected blocks and tests.

**Gotchas:** link rot after renaming blocks; copy-pasted models inheriting wrong links.

Traceability expectations of ISO 26262 parts 8 and 6: confirm in the current edition (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Zero requirements without implementation or verification links (or documented waivers).
- [ ] Every test case traces to at least one requirement.
