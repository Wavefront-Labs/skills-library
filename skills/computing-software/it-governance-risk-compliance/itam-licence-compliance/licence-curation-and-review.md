---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.licence-curation-and-review
name: licence-curation-and-review
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [licence-curation-and-review, software-composition-analysis, curation, false positive, licence finding, concluded licence, review queue, ort curations, clearing, itam-licence-compliance]
level: advanced
status: draft
description: "Review scanner findings, resolve false positives, curate package licence data and record decisions."
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

# Licence findings review and curation

Goal: reliable concluded licences.

Method:
1. Triage findings: unknown, conflicting, or high-risk licences first.
2. Open the source and licence text; confirm declared versus detected licence.
3. Record the concluded licence with justification and reviewer (ORT package curation file, SPDX LicenseConcluded, or tool UI).
4. Reuse curations across projects through a shared repo.
5. Escalate ambiguous cases to legal; create a decision log.
6. Re-review on version upgrade because licences can change.

Gotchas:
- Test and documentation files may be under different licences than the library.
- Matching tools can flag licence mentions in comments as real licences.

Verify: unresolved findings count trends to zero per release.
