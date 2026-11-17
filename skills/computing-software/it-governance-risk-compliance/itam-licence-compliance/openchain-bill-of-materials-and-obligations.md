---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.openchain-bill-of-materials-and-obligations
name: openchain-bill-of-materials-and-obligations
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [openchain-bill-of-materials-and-obligations, openchain-iso-5230, openchain bom, compliance artifacts, licence obligations, third-party content, release review, itam-licence-compliance]
level: practitioner
status: draft
description: "Implement ISO/IEC 5230 processes: BOM per release, licence identification, obligation fulfilment and compliance artefacts."
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

# OpenChain bill of materials and obligation process

Goal: demonstrate relevant tasks are defined and done.

Method:
1. Maintain a process to create and manage an open-source BOM for each supplied software release (name, version, licence, source origin).
2. Review licences against product use-case (distributed, hosted).
3. Prepare compliance artefacts: source code packages, notices, attribution text, written offers.
4. Verify artefacts before release; archive them for a defined period.
5. Include inbound handling of third-party-supplied software (ask suppliers for BOM).

Gotchas:
- Reviews must happen before release, not after.
- Keep identified issues and resolution records.

Verify: pick two releases and trace BOM to published artefacts.
