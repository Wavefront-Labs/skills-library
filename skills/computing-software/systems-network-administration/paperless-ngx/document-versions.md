---
id: computing-software.systems-network-administration.paperless-ngx.document-versions
name: document-versions
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, document-versions, merge-as-versions, update-version, file-history, version-label]
level: practitioner
status: docs-checked
description: "Use document file versions to keep file history under one metadata record, merge documents as versions and handle ASNs and deletion."
sources:
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/api/"
  - "https://docs.paperless-ngx.com/advanced_usage/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Document file versions

Versions are file history for one root document. Tags, correspondent, type, storage path, custom fields and permissions stay shared on the root. The file, mime type, checksums, archive info and extracted text belong to each version. Search and content use the latest version by default.

## UI
- Selecting a version in the detail view switches preview, metadata, content and downloads to it.
- Merge as versions: select two or more documents in the list and pick the root. The others become versions. Documents added as versions cannot have version histories of their own.
- Versions menu > Existing adds another document as a version.
- Deleting a non-root version keeps metadata and falls back to the latest remaining version. Deleting the root trashes its versions too.
- Merging cannot be undone from the UI. Merged documents give up their ASN; if the root has none it takes the first one, otherwise the ASNs are released and the removal is logged.

## Files
Each version uses the normal filename rules with a `_v1`, `_v2` suffix, and a collision counter comes after the suffix.

## API
- `?version={version_id}` on `GET /api/documents/{id}/`, `download`, `preview`, `thumb` and `metadata`.
- `POST /api/documents/{id}/update_version/` with `document` and optional `version_label`.
- `POST /api/documents/merge_as_versions/` with `documents` and `root_document_id`.
- `PATCH` and `DELETE` on `/api/documents/{root_id}/versions/{version_id}/`.

Password-removal workflows also create new versions.

## Checked
2026-11-04. Compared with Document File Versions in usage, the Document Versions section of the API page, and file name handling in advanced usage (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: shared root metadata and permissions, per-version file data, UI behaviour, ASN handling, deletion, _vN suffix with counter after the suffix, all listed endpoints and parameters, password-removal versions. Nothing removed.

Method: documentation only; no commands were run.
