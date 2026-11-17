---
id: computing-software.web-development.ghost.ghost-config-s3-storage-adapter
name: ghost-config-s3-storage-adapter
category: computing-software
field: web-development
product: ghost
tags: [ghost, storage-adapter, s3, cdn, minio, cloudflare-r2, config]
level: advanced
status: docs-checked
description: "Store Ghost images, media and files in S3-compatible storage with the built-in S3Storage adapter, urls and CDN settings."
sources:
  - https://github.com/TryGhost/docs/blob/main/config.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move Ghost uploads to Amazon S3 or an S3-compatible provider.

Ghost ships an `S3Storage` adapter for Amazon S3, MinIO, Google Cloud Storage or Cloudflare R2. Adapters can be set per feature (images, media, files), so you can migrate gradually.

Config shape: `storage.active` names the default adapter, `storage.media` and `storage.files` set an `adapter` per feature, and an `S3Storage` block holds options. Each feature uses a fixed prefix: `content/images`, `content/media`, `content/files`, set through `staticFileURLPrefix`.

Required options: `bucket`, `cdnUrl` (public base URL files are served from), `staticFileURLPrefix`, `multipartUploadThresholdBytes` and `multipartChunkSizeBytes` (at least 5 MiB, 5242880). Optional: `region` (Amazon S3 needs it), `endpoint` (any non-Amazon provider), `forcePathStyle`, `tenantPrefix` (share a bucket between sites), and `accessKeyId` with `secretAccessKey` (give both or neither; otherwise the ambient AWS credential chain is used), plus `sessionToken`.

Also set `urls.image`, `urls.media` and `urls.files` to the public base URLs; without them Ghost will not treat CDN-hosted assets as its own and will not generate responsive sizes.

Warnings: responsive image sizes are generated on demand at `/content/images/size/w600/...` paths, so resizing only works when requests reach Ghost. Switching does not move existing files; copy them into the bucket under the same prefixes first.

Verify: upload an image in the editor and confirm its URL points at your CDN.

## Checked

2026-11-04. Confirmed: supported providers, per-feature adapters, fixed prefixes, the option table (required and optional), urls settings, on-demand resize warning and the existing-files warning (configuration page). Removed: the "active names the images adapter" wording; the page says active is the default for all features.

Method: documentation only; no commands were run.
