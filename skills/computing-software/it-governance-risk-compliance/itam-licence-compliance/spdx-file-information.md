---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.spdx-file-information
name: spdx-file-information
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [spdx-file-information, spdx-document-structure, spdx file, filechecksum, licenseinfoinfile, snippet, filetype, fileattributiontext, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Record per-file checksums, licence information, copyright text and snippets in an SPDX document."
sources:
  - https://github.com/spdx/spdx-spec/blob/support/2.3/chapters/file-information.md
  - https://github.com/spdx/spdx-spec/blob/support/2.3/chapters/snippet-information.md
  - https://github.com/spdx/spdx-spec/blob/support/2.3/chapters/using-SPDX-short-identifiers-in-source-files.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPDX file information and snippets

Goal: file-level provenance where needed.

File fields: FileName, SPDXID, FileChecksum (SHA1 required in 2.3), LicenseConcluded, LicenseInfoInFile, FileCopyrightText; optional FileType (SOURCE, BINARY, TEXT, ARCHIVE, etc.), FileContributor, FileComment, FileNotice.
Snippets: SnippetSPDXID, SnippetFromFile, SnippetByteRange (and optional line range), plus licence concluded for the snippet.

Method:
- Populate LicenseInfoInFile from SPDX-License-Identifier headers and licence-text matches (Annex E describes the header convention).
- Include file-level data when distributing source or needing deep provenance; for ordinary SBOMs package level suffices.

Gotchas:
- File-level lists grow large; include them only when needed.
- FileChecksum must include SHA1 (cardinality 1..1); other algorithms are optional.

Verify: check each field against clauses 8 and 9 of the SPDX 2.3 specification.

## Checked

2026-11-02. Checked against SPDX 2.3 clause 8 (file name, SPDXID, file type values, SHA1 checksum requirement, licence fields, contributor, notice, attribution text), clause 9 (snippet SPDXID, from-file, byte range required, line range optional, concluded licence) and Annex E (SPDX-License-Identifier). Removed: scanner tool names, the hasFiles suggestion and the exact-bytes checksum claim, none of which are in those pages.

Method: documentation only; no commands were run.
