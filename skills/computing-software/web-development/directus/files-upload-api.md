---
id: computing-software.web-development.directus.files-upload-api
name: files-upload-api
category: computing-software
field: web-development
product: directus
tags: [file-upload, multipart-upload, storage-location, public-upload-risk]
level: practitioner
status: docs-checked
description: "Upload files to Directus via the Studio or POST /files multipart/form-data, set properties and the storage location, and avoid risky public uploads."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/05.files/1.upload.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Any kind of file, several at once, can be uploaded.

**Studio**: Files module > open or create a folder > add button > drag a file, click to select, or use the popup menu's **Import from URL**.

**API**: `POST /files` with a `multipart/form-data` body where the file content is in a property named `file`. The body ends with a final `file` property; the page's example appends each file's other properties before its `file` entry. Other file object properties can be sent, except `filename_disk` and `filename_download`.

```js
import { createDirectus, rest, uploadFiles } from '@directus/sdk';
const directus = createDirectus('https://directus.example.com').with(rest());
const formData = new FormData();
formData.append('title', 'My file');
formData.append('file', rawFile);
await directus.request(uploadFiles(formData));
```

GraphQL does not support uploads.

Gotchas:
- If `storage` is omitted, the first location in `STORAGE_LOCATIONS` is used. A given `storage` must match a configured location exactly, including case, or you get `INVALID_PAYLOAD`.
- If you allow uploads from the public role or unauthenticated users, read the security best practices on restricting public file uploads first.

## Checked

2026-11-04: Studio upload options, POST /files multipart body with the file property, excluded filename properties, SDK uploadFiles, GraphQL not supported, the STORAGE_LOCATIONS default with INVALID_PAYLOAD and the public upload warning confirmed against the Directus Upload Files page. Reworded the property ordering note and removed a Verify line the page does not state.

Method: documentation only; no commands were run.
