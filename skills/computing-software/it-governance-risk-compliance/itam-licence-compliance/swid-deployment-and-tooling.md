---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.swid-deployment-and-tooling
name: swid-deployment-and-tooling
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [swid-deployment-and-tooling, swid-tags-iso-19770-2, swid generation, swid directory, tag collection, software inventory, silverlining, itam-licence-compliance]
level: advanced
status: draft
description: "Place SWID tags in standard directories, generate them in builds and collect them with discovery for software inventory."
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

# Deploying and consuming SWID tags

Goal: authoritative, vendor-supplied software identity in inventory.

Method:
- Installers write the primary tag to a defined location (platform conventions, e.g. under a swidtag directory of the program data area; confirm per OS and standard).
- Build pipeline: generate SWID with each release, sign the tag (XML digital signature) so tampering is detectable.
- Discovery tools collect tags and match them to normalised software titles, avoiding string-based matching.
- NIST NISTIR 8060 describes how SWID supports cybersecurity (vulnerability matching).
- Map tagId to SPDX package or CPE for cross-use.

Gotchas:
- Unsigned tags can be forged.
- Version strings must follow the declared versionScheme.

Verify: inventory shows installed titles matched by tagId and vendor.
