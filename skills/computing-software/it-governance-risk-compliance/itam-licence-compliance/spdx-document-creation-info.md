---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.spdx-document-creation-info
name: spdx-document-creation-info
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [spdx-document-creation-info, spdx-document-structure, spdx, spdx 2.3, document creation, documentnamespace, spdxid, datalicense, cc0-1.0, creator, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Fill in SPDX document creation fields: spdxVersion, dataLicense, SPDXID, name, documentNamespace, creators and created."
sources:
  - https://github.com/spdx/spdx-spec/blob/support/2.3/chapters/document-creation-information.md
  - https://github.com/spdx/spdx-spec/blob/support/2.3/chapters/conformance.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPDX document creation information

Goal: valid SPDX 2.3 document headers.

Mandatory fields (SPDX 2.3):
- spdxVersion: "SPDX-2.3".
- dataLicense: CC0-1.0.
- SPDXID: SPDXRef-DOCUMENT.
- name: document name.
- documentNamespace: a unique URI per document version (used by external references).
- creators ("Person: name" or "Organization: name", each with optional email, and "Tool: toolidentifier-version") and created timestamp formatted YYYY-MM-DDThh:mm:ssZ (e.g. 2025-01-31T12:00:00Z).
Optional: creatorComment, licenseListVersion, externalDocumentRefs.

Formats: tag-value, JSON, YAML, RDF/XML, spreadsheet.

Gotchas:
- Each new version of a document needs a new documentNamespace; the URI must not contain a "#".
- Timestamp must end in Z.

Verify: check each field against clause 6 of the SPDX 2.3 specification.

## Checked

2026-11-02. Checked against SPDX 2.3 clause 6 (version, data licence, SPDXID, name, namespace, external document references, licence list version, creator, created, creator comment) and the conformance clause (formats). Removed: the online validator and tools-java / pyspdxtools line (not in the spec) and the made-up tool identifier.

Method: documentation only; no commands were run.
