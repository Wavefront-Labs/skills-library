---
id: computing-software.cloud-infrastructure-engineering.zot.s3-storage-backend
name: s3-storage-backend
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, s3-storage, storage-driver, redirect-blob-url, minio, iam-permissions]
level: practitioner
status: docs-checked
description: "Configure Zot's S3 or S3-compatible storageDriver: required keys, defaults, credentials, IAM needs, redirectBlobURL, and the Windows warning."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/storage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `storage.storageDriver` with `name: s3`. Required: `name`, `region`, `bucket`.

Defaults and options:
- `accesskey`, `secretkey`: optional; omit to use IAM roles or environment/credentials files.
- `regionendpoint`: for MinIO and similar.
- `forcepathstyle` true; `secure` true (HTTPS); `skipverify` false; `v4auth` true.
- `encrypt` false; `keyid` (KMS) ignored unless `encrypt` is true.
- `chunksize` must exceed 5 x 1024 x 1024.
- `storageclass` `STANDARD`; `objectacl` `private`; `loglevel` `off`.
- Others: `rootdirectory` (key prefix), `multipartcopychunksize`, `multipartcopymaxconcurrency`, `multipartcopythresholdsize`, `useragent`, `usedualstack`, `accelerate`.

Credentials: environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, optional `AWS_SESSION_TOKEN`) or the `credentials` file in the `.aws/` home subdirectory (`[default]` profile unless `AWS_PROFILE` is set).

IAM needs bucket-level list and location actions and object-level put, get, delete, multipart list and abort actions.

`storage.redirectBlobURL: true` (any remote backend, global or per subpath) makes blob pulls return `307` to signed backend URLs, cutting proxy traffic; it falls back to proxying if URL generation fails.

Warning: do not use the S3 driver on Windows; it can hang at startup, exhaust memory and burn CPU.

## Checked

2026-11-04. Read against the zot storage planning article (s3 attributes, credentials, permissions, redirect sections); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
