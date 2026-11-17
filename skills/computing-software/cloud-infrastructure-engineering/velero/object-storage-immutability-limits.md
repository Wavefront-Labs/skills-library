---
id: computing-software.cloud-infrastructure-engineering.velero.object-storage-immutability-limits
name: object-storage-immutability-limits
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [immutability, object-lock, finalizing, worm, backup-storage]
level: advanced
status: docs-checked
description: "Why Velero 1.11+ backups can break on immutable or object-lock buckets, and how AWS S3, Azure Blob and GCP behave."
sources:
  - https://velero.io/docs/main/backup-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Velero does not support backup data immutability. From 1.11, a backup first saves its state as Finalizing, then checks for async operations still running. If there are any, Velero waits for them before moving the backup to Complete; if none, it moves to Complete straight away. Either way Velero must modify metadata in object storage, which is not possible if immutability is configured.

Before 1.11 there was also no explicit support. You may see problems even though backups seem to work, for example versioned objects not being deleted when a backup is deleted. Backups can still work in some cases depending on provider and configuration.

Provider behaviour:
- AWS S3: backups work because S3 Object Lock applies only to versioned buckets and the data can still be updated as a new version. When a backup is deleted, old versions of the objects are not deleted.
- Azure Storage Blob: version-level immutability can still work with Velero; container-level immutability cannot.
- GCP Cloud Storage: only bucket-level retention policies exist, so there is no way to make it work.

The Velero docs link the provider pages: AWS S3 Using S3 Object Lock, Azure Storage Blob Lock Immutability Policy, and GCP Retention policies and retention policy locks.

## Checked

Checked 2026-11-08 against the Velero Backup Reference page ("Cannot support backup data immutability", read in full). Removed the unsourced "practical rule" paragraph (separate immutable bucket advice) and wrote the state name as Complete, as the page does. Provider pages were not fetched; only the Velero page's statements about them are relayed.

Method: documentation only; no commands were run.
