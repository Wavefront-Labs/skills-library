---
id: computing-software.web-development.payload-cms.upload-collections
name: upload-collections
category: computing-software
field: web-development
product: payload-cms
tags: [uploads, upload-collection, staticdir, mimetypes]
level: practitioner
status: docs-checked
description: "Enable file uploads on a collection with the upload option, including staticDir, mimeTypes, adminThumbnail and other collection upload options."
sources:
  - https://payloadcms.com/docs/upload/overview
  - https://payloadcms.com/docs/upload/transformers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upload collections

Goal: turn a Collection into a media library.

```ts
export const Media: CollectionConfig = {
  slug: 'media',
  upload: {
    staticDir: 'media',
    adminThumbnail: 'thumbnail',
    mimeTypes: ['image/*'],
  },
  fields: [{ name: 'alt', type: 'text' }],
}
```

Payload adds `filename`, `mimeType` and `filesize` fields, thumbnails in the List View, upload UI in the edit view, and file handling in create, update and delete. `upload: true` uses defaults.

Collection upload options: `adminThumbnail`, `bulkUpload` (default true), `cacheTags`, `crop`, `disableLocalStorage`, `displayPreview`, `externalFileHeaderFilter`, `filesRequiredOnCreate` (default true), `filenameCompoundIndex`, `focalPoint`, `handlers`, `mimeTypes`, `pasteURL` (enabled by default), `skipSafeFetch`, `allowRestrictedFileTypes` (default false), `staticDir`, `hideFileInputOnCreate`, `hideRemoveFile`, `modifyResponseHeaders`.

- `staticDir` may be absolute or relative to the config; it defaults to the collection slug.
- Image sizes and cropping are configured through the Sharp transformer, not on the collection.
- Install `@payloadcms/transformer-sharp` for image resizing and register it under `upload.transformers`.
- Uploads work through REST, Local API and MCP, not GraphQL. Over REST, send `multipart/form-data` with a `file` key and any other fields as a JSON string in `_payload`.
- Restricted file types (executables, scripts, HTML and similar) are rejected unless the collection sets `mimeTypes` or `allowRestrictedFileTypes: true`.
- `disableLocalStorage: true` breaks Admin thumbnails unless you store files elsewhere and supply `adminThumbnail`.

Verify: upload an image in the Admin Panel and fetch `/api/media/file/<filename>`.

## Checked

2026-11-04. Read upload/overview and upload/transformers. Confirmed: the added filename, mimeType and filesize fields, the media collection example, every collection upload option listed with its default (bulkUpload true, filesRequiredOnCreate true, pasteURL enabled by default, skipSafeFetch false, allowRestrictedFileTypes false), staticDir defaulting to the collection slug and being absolute or relative to the config, Sharp options being set through sharpTransformer rather than the collection, and the file endpoint /api/<collection>/file/<filename>. Corrected: the sharp install instruction now names @payloadcms/transformer-sharp as the transformers page does. Added: GraphQL and REST upload notes, restricted file types, and disableLocalStorage thumbnails.
Method: documentation only; no commands were run.
