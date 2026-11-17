---
id: computing-software.web-development.payload-cms.upload-storage-adapters
name: upload-storage-adapters
category: computing-software
field: web-development
product: payload-cms
tags: [storage-adapters, s3-storage, vercel-blob, clientuploads]
level: practitioner
status: docs-checked
description: "Store uploads in S3, Vercel Blob, Azure, GCS or R2 by registering a storage adapter under the top-level storage config key."
sources:
  - https://payloadcms.com/docs/upload/storage-adapters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Storage adapters

Goal: store files outside the server filesystem.

Official packages: `@payloadcms/storage-vercel-blob`, `@payloadcms/storage-s3`, `@payloadcms/storage-azure`, `@payloadcms/storage-gcs`, `@payloadcms/storage-r2`. The R2 adapter is for Cloudflare Workers only; elsewhere use `@payloadcms/storage-s3` against the R2 S3 endpoint (`region: 'auto'`, `forcePathStyle: true`, `endpoint`), and serve files through a public R2 domain with `generateFileURL`.

Register adapters under the top-level `storage` key:

```ts
import { s3Storage } from '@payloadcms/storage-s3'

export default buildConfig({
  storage: [
    s3Storage({
      bucket: process.env.S3_BUCKET,
      collections: { media: true },
      config: { region: process.env.S3_REGION },
    }),
  ],
})
```

`collections` maps slugs to `true` or to per-collection options such as `{ prefix: 'my-prefix' }` (Vercel Blob example). `enabled` is optional and defaults to true. Each adapter sets `disableLocalStorage` to true for its collections. Vercel limits server uploads to 4.5MB, so set `clientUploads: true` there (S3 also needs CORS `PUT` and the `If-None-Match` header allowed).

If your config still registers adapters in `plugins`, run `npx @payloadcms/codemod --transform migrate-storage-adapters-to-config`.

Upload instructions: the Admin asks `POST /api/upload-instructions` how to upload, Payload checks access and file limits, and the Admin follows the adapter's instructions. With `clientUploads` enabled, S3, Azure and GCS upload directly to storage rather than through Payload (useful on serverless request-size limits).

Verify: after an upload, the object appears in the bucket or blob store and no file is written to the collection's local `staticDir`.

## Checked

2026-11-04. Read upload/storage-adapters. Confirmed: the package table, top-level storage key and the codemod command, the upload-instructions flow with POST /api/upload-instructions, clientUploads for S3, Azure and GCS, collections as true or per-collection options such as prefix, the optional enabled flag, automatic disableLocalStorage, the 4.5MB Vercel limit, and the R2 note that storage-r2 is for Workers only. Changed: the verify step, because default URLs go through Payload's file route unless a direct URL is configured.
Method: documentation only; no commands were run.
