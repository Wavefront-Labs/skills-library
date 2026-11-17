---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.spdx-package-information
name: spdx-package-information
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [spdx-package-information, spdx-document-structure, spdx package, downloadlocation, filesanalyzed, packageverificationcode, licenseconcluded, licensedeclared, supplier, purl, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Describe packages with name, version, supplier, downloadLocation, filesAnalyzed, verification code and licence fields."
sources:
  - https://github.com/spdx/spdx-spec/blob/support/2.3/chapters/package-information.md
  - https://github.com/spdx/spdx-spec/blob/support/2.3/chapters/external-repository-identifiers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPDX package information

Goal: complete, interoperable package entries.

Required in 2.3 (field tables): PackageName, SPDXID (SPDXRef-...) and PackageDownloadLocation (URL, NONE or NOASSERTION). FilesAnalyzed is optional and defaults to true. PackageVerificationCode is allowed only when FilesAnalyzed is true or omitted, and must be omitted when it is false (such a package cannot contain files). Everything else is optional: PackageVersion, PackageSupplier, PackageChecksum (algorithm:value, e.g. SHA1 or SHA256), PackageLicenseConcluded, PackageLicenseDeclared, PackageLicenseInfoFromFiles, PackageCopyrightText, ExternalRef.
ExternalRef has the form category type locator, with category SECURITY, PACKAGE-MANAGER, PERSISTENT-ID or OTHER. Use PACKAGE-MANAGER with type purl (pkg:npm/lodash@4.17.21), or SECURITY with type cpe23Type.

Concluded versus declared: declared is what the authors state; concluded is your analysis result.

Gotchas:
- Use NOASSERTION where the field allows it and the value is unknown (supplier, download location, licence fields).
- The verification code covers the package's files except the SPDX document itself (excluded files are named alongside the code).

Verify: compare each field with clause 7 of the SPDX 2.3 specification.

## Checked

2026-11-02. Checked against SPDX 2.3 clause 7 (required flags and cardinality of each package field, FilesAnalyzed default, verification code algorithm and condition, checksum format, supplier NOASSERTION, ExternalRef format) and Annex F (cpe23Type under Security, purl under Package-Manager). Fixed: the skill listed FilesAnalyzed, licence fields, copyright text and verification code as required; the spec marks them optional (verification code conditional). Removed: the claim that SHA1 is the minimum package checksum.

Method: documentation only; no commands were run.
