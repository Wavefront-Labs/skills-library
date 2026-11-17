---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.chain-of-custody-and-onsite-destruction
name: chain-of-custody-and-onsite-destruction
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [chain-of-custody-and-onsite-destruction, itad-and-disposal, chain of custody, sealed container, manifest, onsite shredding, witnessed destruction, itam-licence-compliance]
level: practitioner
status: draft
description: "Control custody from decommission to destruction with sealed containers, manifests and optional witnessed on-site shredding."
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

# Chain of custody and on-site destruction

Goal: no unaccounted hand-off.

Method:
1. Decommission: remove from CMDB duty, record serials into a manifest.
2. Pack in tamper-evident, numbered containers; log seal numbers.
3. Hand-over signed by both parties; vendor GPS-tracked vehicles.
4. Intake scan at vendor matches manifest; exceptions raised within 48 hours.
5. High-risk media: witnessed on-site shredding with particle size specification (confirm per classification).

Gotchas:
- Staging rooms with unlocked devices are the usual leak point.
- Update asset status to Disposed only after certificate receipt.

Verify: manifest, intake report and certificate all show identical serial lists.
