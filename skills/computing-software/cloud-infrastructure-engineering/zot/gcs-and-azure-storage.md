---
id: computing-software.cloud-infrastructure-engineering.zot.gcs-and-azure-storage
name: gcs-and-azure-storage
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, gcs-storage, azure-blob, storage-driver, application-default-credentials]
level: practitioner
status: docs-checked
description: "Configure Zot remote storage on Google Cloud Storage or Azure Blob Storage: driver names, required keys, credential types and root directory defaults."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/storage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both use `storage.storageDriver` and follow the same remote-storage behaviour as S3. Dedupe is supported on cloud backends.

Google Cloud Storage (`name: gcs`):
- `bucket`: required.
- `rootdirectory`: optional; defaults to `/zot`, and a value of `/` is overridden with that default.
- `keyfile`: optional; omit when using Application Default Credentials.

Azure Blob Storage (`name: azure`), based on the distribution v3 driver:
- `accountname`: required.
- `container`: required.
- `rootdirectory`: optional prefix; if omitted Zot uses `/zot`-like semantics.
- `credentials.type`: required; one of `shared_key`, `client_secret`, `default_credentials`.

Tips:
- Pair either with a cache driver (DynamoDB or Redis) if more than one Zot instance shares the bucket; the default BoltDB cache does not support concurrent writers.
- `redirectBlobURL` works with remote backends to send clients to signed URLs.
- For sync staging (streaming on-demand), S3, GCS and Azure need `extensions.sync.downloadDir`.

## Checked

2026-11-04. Read against the zot storage planning article (GCS, Azure) and mirroring article (downloadDir); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
