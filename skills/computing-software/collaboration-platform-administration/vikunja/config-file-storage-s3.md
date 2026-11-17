---
id: computing-software.collaboration-platform-administration.vikunja.config-file-storage-s3
name: config-file-storage-s3
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, files-section, s3-backend, usepathstyle, disablesigning, max-upload-size]
level: practitioner
status: docs-checked
description: "Choose local or S3-compatible attachment storage for Vikunja and set the upload size limit, path style and signing options for MinIO, Ceph or Backblaze."
sources:
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/config.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`files.type` is `local` (default) or `s3`.

Local: `files.basepath` default `./files`; a relative path is resolved against `service.rootpath`. `files.maxsize` default `20MB` (human-readable string).

S3 options under `files.s3`:
- `endpoint`: can be used with S3-compatible services such as MinIO or Backblaze B2.
- `bucket`, `region`, `accesskey`, `secretkey`.
- `usepathstyle` default false: path-style addressing (for example `https://s3.amazonaws.com/bucket/key`) instead of virtual-hosted style (`https://bucket.s3.amazonaws.com/key`); commonly needed for self-hosted S3-compatible services, and some providers support only one style.
- `disablesigning` default false: sends UNSIGNED-PAYLOAD instead of computing a SHA256 hash. Works around `XAmzContentSHA256Mismatch` errors with providers such as Ceph RadosGW and Clever Cloud Cellar. Only applies over HTTPS.

Any config value can be read from a file with the `file` child key, or the `_FILE` environment suffix (for example `VIKUNJA_DATABASE_PASSWORD_FILE`); apply this to the S3 keys to keep them out of the config file.

Task attachments can be disabled with `service.enabletaskattachments` (default true).

## Checked

2026-11-04: checked against config-raw.json (files, files.s3, service.enabletaskattachments) and the config page (basepath resolution, `_FILE`). Removed the nginx `client_max_body_size` advice and the generic backup line, which no source states.

Method: documentation only; no commands were run.
