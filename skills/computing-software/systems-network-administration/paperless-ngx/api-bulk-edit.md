---
id: computing-software.systems-network-administration.paperless-ngx.api-bulk-edit
name: api-bulk-edit
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, bulk-edit, api, set-permissions, modify-tags, bulk-edit-objects]
level: advanced
status: docs-checked
description: "Edit many documents or objects at once with /api/documents/bulk_edit/ and /api/bulk_edit_objects/, including the supported methods."
sources:
  - "https://docs.paperless-ngx.com/api/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bulk editing through the API

Operations run asynchronously.

## Documents
```json
POST /api/documents/bulk_edit/
{"documents": [1, 2, 3], "method": "add_tag", "parameters": {"tag": 5}}
```
Methods and parameters:
- `set_correspondent` (`correspondent`), `set_document_type` (`document_type`), `set_storage_path` (`storage_path`)
- `add_tag`, `remove_tag` (`tag`)
- `modify_tags` (`add_tags`, `remove_tags` as ID lists)
- `delete` (no parameters)
- `reprocess` (optional `remote_ocr: true`)
- `set_permissions` (`set_permissions`, `owner`, and `merge`; merge defaults to false, which overwrites existing permissions)
- `modify_custom_fields` (`add_custom_fields` as an id-to-value object or list of IDs, `remove_custom_fields`)

Permission payloads use `{"view": {"users": [], "groups": []}, "change": {...}}` with numeric IDs.

## Document editing
From API version 10, merge, rotate and edit_pdf have their own endpoints, documented in the API spec. The legacy methods through `bulk_edit` still work but are deprecated.

## Objects
```json
POST /api/bulk_edit_objects/
{"objects": [1, 2], "object_type": "tags", "operation": "delete"}
```
`object_type` is tags, correspondents, document_types or storage_paths. Operations are `set_permissions` or `delete`; `set_permissions` takes `owner`, `permissions` and `merge`.

Setting permissions requires being the owner or a superuser.

## Checked
2026-11-04. Compared line by line with the Bulk Editing section of the API page (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: both endpoints, every method name and its parameters, the merge default, document-editing endpoints from version 10 with legacy methods deprecated, object types and operations, owner/superuser requirement for setting permissions. Nothing removed.

Method: documentation only; no commands were run.
