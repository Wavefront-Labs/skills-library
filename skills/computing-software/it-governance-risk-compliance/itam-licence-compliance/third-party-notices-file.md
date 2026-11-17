---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.third-party-notices-file
name: third-party-notices-file
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [third-party-notices-file, permissive-compliance-practice, third party notices, attribution, notice file, licence text, copyright holder, open source disclosure, itam-licence-compliance]
level: practitioner
status: draft
description: "Generate a complete third-party notices file with licence texts and copyright holders for each shipped component."
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

# Building a third-party notices file

Goal: automated compliance with attribution duties.

Method:
1. Produce the dependency inventory from the build (SBOM).
2. For each component, collect SPDX licence ID, licence text, copyright line and NOTICE file.
3. Generate a notices file using tools (for example license-checker, cargo-about, go-licenses, pip-licenses, ORT NoticeGenerator; confirm tool options).
4. Deduplicate identical licence texts and group components.
5. Ship the file in product docs, About screen or a URL printed in the manual.

Gotchas:
- Transitive and vendored dependencies are often missed.
- Frontend bundles include minified licences; keep banner comments or give a separate file.

Verify: spot-check 10 components for correct text and copyright holder.
