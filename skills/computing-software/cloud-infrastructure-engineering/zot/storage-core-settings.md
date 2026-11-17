---
id: computing-software.cloud-infrastructure-engineering.zot.storage-core-settings
name: storage-core-settings
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, storage-config, dedupe, commit, hydrate-blob-on-read, fast-restart, root-directory]
level: practitioner
status: docs-checked
description: "Zot storage block basics: rootDirectory, commit, dedupe, hydrateBlobOnRead, fastRestart, supported backends and the OCI layout on disk."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/storage.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/admin-guide/admin-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Zot speaks the OCI Distribution Spec on the wire and stores the OCI Image Layout on disk.

Backends: local filesystem (at least one root directory; NFS and FUSE mounts count as local), AWS S3 and S3-compatible storage, Google Cloud Storage, Azure Blob Storage. S3 is not supported on Windows.

Key `storage` attributes:
- `rootDirectory`: where images live on the server filesystem.
- `commit`: default `false`; writes data to disk immediately (useful on low-RAM devices). From v2.1.23 it also syncs the directory on committed local renames.
- `dedupe`: enabled by default; one copy of identical content using hard links on local storage (needs hard-link support). On startup Zot enforces the current dedupe status on existing storage.
- `hydrateBlobOnRead` (v2.1.21+): default `false`, so blob reads are repository-local and return `404` until the blob is mounted or uploaded into that repository. `true` creates a repository-local hard link from the dedupe cache on read. Prefer explicit cross-repository mounts for new integrations.
- `fastRestart`: default `false`; can skip the startup storage walk when a stamp matches. Out-of-band changes made while Zot was down are not detected.
- `maxRepos`: a push creating a new repository beyond the limit returns `413`.

## Checked

2026-11-04. Read against the zot storage planning article; every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
