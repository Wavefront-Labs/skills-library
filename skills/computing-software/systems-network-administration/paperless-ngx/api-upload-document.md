---
id: computing-software.systems-network-administration.paperless-ngx.api-upload-document
name: api-upload-document
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, post-document, file-upload, api, consumption-task, multipart]
level: practitioner
status: docs-checked
description: "Upload a document through POST /api/documents/post_document/ with optional metadata fields, then poll the returned task id."
sources:
  - "https://docs.paperless-ngx.com/api/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Uploading through the API

POST a multipart form to `/api/documents/post_document/`. The `document` field holds the file; its name is sanitised and it is stored in a temporary directory for the consumer.

## Optional fields
- `title`
- `created` (for example `2016-04-19` or `2016-04-19 06:15:00+02:00`)
- `correspondent`, `document_type`, `storage_path` as IDs
- `tags`, repeated for several tags
- `archive_serial_number`
- `custom_fields`: an array of field IDs (empty values) or an object mapping field id to value

```bash
curl -H "Authorization: Token <TOKEN>" \
  -F "document=@/path/to/scan.pdf" \
  -F "title=Invoice 42" -F "tags=3" -F "tags=7" \
  https://paperless.example.com/api/documents/post_document/
```

## Response and status
HTTP 200 means the consume task started; the body is the task UUID. Nothing else is known immediately because consumption happens in another process. Query:
```
/api/tasks/?task_id=<UUID>
```
for the state, including the created document ID on success.

## Versions
`POST /api/documents/{id}/update_version/` uploads a new file version with the `document` field and an optional `version_label`.

## Duplicates
In v3 a duplicate upload is consumed unless `PAPERLESS_CONSUMER_DELETE_DUPLICATES=true`, in which case the task fails.

## Checked
2026-11-04. Compared with the POSTing documents section of the API page, the duplicate section of usage and the v3 migration page (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: endpoint, form fields, date examples, repeated tags, custom_fields forms, HTTP 200 with task UUID, task lookup URL, update_version, v3 duplicate behaviour and the delete-duplicates setting. Nothing removed.

Method: documentation only; no commands were run.
