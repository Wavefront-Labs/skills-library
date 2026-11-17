---
id: computing-software.database-administration.supabase.resumable-uploads
name: resumable-uploads
category: computing-software
field: database-administration
product: supabase
tags: [storage, resumable-uploads, tus, chunk-size, upsert]
level: practitioner
status: docs-checked
description: "Upload large Supabase Storage files with TUS resumable uploads: endpoint, headers, 6MB chunks, retry delays, 24 hour URLs and conflict behaviour."
sources:
  - https://supabase.com/docs/guides/storage/uploads/resumable-uploads
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: upload big files reliably over flaky networks.

Recommended for files over 6MB or when stability is a concern.

Endpoint: `https://project-id.storage.supabase.co/storage/v1/upload/resumable`. Use the direct storage hostname, not `project-id.supabase.co`.

Headers:
- `Authorization: Bearer <access token>`.
- `x-upsert: true` (optional) overwrites an existing file.
- `x-signature` carries the token from `createSignedUploadUrl` for presigned uploads.
- Uppy's React example also sends an `apikey` header.

Client options (JavaScript):
- `chunkSize: 6 * 1024 * 1024`; the page says it "must be set to 6MB (for now)".
- `retryDelays: [0, 3000, 5000, 10000, 20000]`.
- `uploadDataDuringCreation: true`.
- `removeFingerprintOnSuccess: true`, needed to re-upload the same file.
- Metadata: `bucketName`, `objectName`, `contentType`, `cacheControl`, `metadata` (a JSON string stored in the `user_metadata` column).

Behaviour:
- Each upload has its own URL; chunks are sent with `PATCH`.
- An upload URL is valid up to 24 hours, then the upload restarts; TUS clients usually create a new URL automatically.
- Only one client can use a given URL; others get `409 Conflict`.
- For the same path through different URLs, the first to finish wins and the rest get `409`; with `x-upsert`, the last to finish wins.
- An existing path without `x-upsert` returns `400 Asset Already Exists`.
- Overwriting is discouraged because CDN propagation serves stale content; upload to a new path.

## Checked

Confirmed against the page source: direct storage hostname and endpoint, headers (authorization, x-upsert, x-signature, apikey in the Uppy example), 6MB chunk size, retryDelays, uploadDataDuringCreation, removeFingerprintOnSuccess, metadata fields, PATCH chunks, 24 hour URL validity, 409 Conflict and 400 Asset Already Exists rules, CDN staleness advice. Nothing removed.

Method: docs-checked 2026-11-09 against the Supabase docs source for guides/storage/uploads/resumable-uploads (apps/docs/content on GitHub master), read in full.
