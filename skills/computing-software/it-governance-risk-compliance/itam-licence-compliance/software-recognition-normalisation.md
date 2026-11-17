---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.software-recognition-normalisation
name: software-recognition-normalisation
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [software-recognition-normalisation, sam-process-and-licence-position, normalisation, software recognition, catalogue, publisher, edition, install string, itam-licence-compliance]
level: practitioner
status: draft
description: "Normalise raw install strings into vendor, product, edition and version using a catalogue with manual overrides."
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

# Software recognition and normalisation

Goal: reliable product identity so licence counts are right.

Method:
- Source signals: SWID, add/remove programs, package managers, file signatures, service names.
- Match to a catalogue (vendor-provided recognition library or in-house) producing publisher, product, edition, version.
- Maintain override rules for unmatched items; review the top unrecognised list weekly.
- Exclude free components (runtimes, drivers) via rule groups.

Gotchas:
- Editions (Standard vs Enterprise) can look identical in installed names; use feature flags or licence keys.
- Vendors rename products after acquisitions.

Verify: recognition rate exceeds 95% on licensable titles.
