---
id: computing-software.devops-ci-cd.forgejo.storage-local-and-minio
name: storage-local-and-minio
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [storage-subsystems, minio-storage, s3-storage, storage-path]
level: practitioner
status: docs-checked
description: "Control where attachments, LFS, avatars, packages and Actions data live: local paths or S3-compatible minio."
sources:
  - https://forgejo.org/docs/latest/admin/setup/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each storage subsystem keeps its files in a dedicated directory, on local disk (the default) or on an S3-compatible server (type `minio`). The subsystems and directories are: attachments, lfs, avatars, repo-avatars, repo-archive, packages, actions_log and actions_artifacts, with sections `[attachment]`, `[lfs]`, `[avatar]`, `[repo-avatar]`, `[repo-archive]`, `[packages]`, `[storage.actions_log]` and `[actions.artifacts]`.

The `[storage]` section changes all of them. Local mode only allows `PATH` (absolute), so `PATH = /mystorage` puts attachments in `/mystorage/attachments`. For minio set `STORAGE_TYPE = minio`, `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY_ID`, `MINIO_SECRET_ACCESS_KEY`, `MINIO_BUCKET` and `MINIO_LOCATION`; each subsystem becomes a directory (prefix) in the bucket. `MINIO_BASE_PATH` must not be set in `[storage]`; it is only valid in a subsystem section, where it overrides the default directory. `MINIO_USE_SSL` defaults to `false` to stay compatible with locally hosted MinIO; set it to `true` when using an external S3 provider.

A single subsystem can differ, for example `[attachment] PATH = /otherstorage/attachments` while `[lfs]` uses minio with `MINIO_BASE_PATH = lfs/`.

With minio, the default directory for attachments in the bucket is `attachments/`.

## Checked

Date: 2026-11-07
Confirmed against the "Storage settings" page, read in full (code blocks included): the subsystem, directory and section table, local `PATH` semantics and the `/mystorage/attachments` example, the minio setting names, `MINIO_BASE_PATH` rules, the `MINIO_USE_SSL` default and the single-subsystem example.
Corrected: `MINIO_USE_SSL` "must be true" for external providers is "should be set to true" on the page. Removed the backup-plan sentence (not on this page).
Method: documentation only; no commands were run.
