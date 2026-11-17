---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.spdx-licence-list-and-licenseref
name: spdx-licence-list-and-licenseref
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [spdx-licence-list-and-licenseref, spdx-relationships-and-licences, spdx license list, licenseref, hasextractedlicensinginfos, exception list, deprecated ids, matching guidelines, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Use SPDX licence IDs, LicenseRef- identifiers with extracted text, and the exception list in licensing fields."
sources:
  - https://github.com/spdx/spdx-spec/blob/support/2.3/chapters/other-licensing-information-detected.md
  - https://github.com/spdx/spdx-spec/blob/support/2.3/chapters/license-matching-guidelines-and-templates.md
  - https://github.com/spdx/license-list-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPDX Licence List, LicenseRef and exceptions

Goal: standardised licence identification.

- Use IDs from the SPDX License List (spdx.org/licenses); each has an exact ID, name, OSI/FSF flags and deprecation status.
- Unlisted or custom licences: use LicenseRef-<idstring> and include text in hasExtractedLicensingInfos (extractedText, name, seeAlsos).
- Exceptions use WITH and the exceptions list (Classpath-exception-2.0, LLVM-exception).
- Matching guidelines: whitespace and punctuation normalisation, replaceable text, optional text; use them for comparing license texts.
- NOASSERTION/NONE are sentinel values for unknown/none.

Gotchas:
- Don't invent IDs; custom ones must start with LicenseRef-.
- License list versions change; record licenseListVersion.

Verify: all IDs resolve in the current list.

## Checked

2026-11-02. Checked against SPDX 2.3 clause 10 (LicenseRef-idstring, extracted text, name, cross references), Annex B (whitespace, replaceable and optional text guidelines), clause 6.7 (licence list version), the 2.3 JSON schema (hasExtractedLicensingInfos with extractedText, name, seeAlsos) and spdx/license-list-data (licenseId, name, isOsiApproved, isFsfLibre, isDeprecatedLicenseId; Classpath-exception-2.0 and LLVM-exception exist). Nothing removed.

Method: documentation only; no commands were run.
