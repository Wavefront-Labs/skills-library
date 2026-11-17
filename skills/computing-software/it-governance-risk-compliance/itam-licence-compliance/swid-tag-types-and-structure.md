---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.swid-tag-types-and-structure
name: swid-tag-types-and-structure
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [swid-tag-types-and-structure, swid-tags-iso-19770-2, swid, software identification tag, corpus tag, primary tag, patch tag, supplemental tag, tagid, itam-licence-compliance]
level: practitioner
status: draft
description: "Understand corpus, primary, patch and supplemental SWID tags and the required XML elements such as tagId and softwareIdentity."
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

# SWID tag types and structure

Goal: read and author SWID tags for software identification.

Tag types:
- Corpus: describes software before installation (installer).
- Primary: describes installed software.
- Patch: indicates a patch is applied.
- Supplemental: adds data to another tag (e.g. by a third party).

Key fields in the SoftwareIdentity element: tagId (globally unique), name, version, versionScheme (e.g. multipartnumeric, semver), tagVersion, plus Entity elements with role (tagCreator, softwareCreator, licensor, aggregator, distributor).
Link elements express relationships (installationmedia, parent, patches, supplements).

Gotchas:
- tagId must stay stable across tag-file edits; version changes belong in version, not tagId.
- Many commercial installers do not ship tags; do not assume absence means absence of software.

Verify: validate against the ISO 19770-2:2015 XML schema.
