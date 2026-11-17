---
id: computing-software.cloud-infrastructure-engineering.velero.backup-storage-locations
name: backup-storage-locations
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [backup-location, backupstoragelocation, bsl, default-location, storage-location]
level: practitioner
status: docs-checked
description: "Create several Velero BackupStorageLocations, set the default with backup-location set, and pick one per backup with --storage-location."
sources:
  - https://velero.io/docs/main/locations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `BackupStorageLocation` (BSL) is a bucket, or a prefix within one, plus provider-specific fields such as the AWS region. Velero assumes it controls the location, so use a dedicated bucket or prefix; with a prefix the rest of the bucket stays free for other uses.

Create two locations in one account:

```shell
velero backup-location create backups-primary \
    --provider aws --bucket velero-backups \
    --config region=us-east-1 --default
velero backup-location create backups-secondary \
    --provider aws --bucket velero-backups \
    --config region=us-west-1
```

The default BSL receives backups when none is named. Change it any time:

```shell
velero backup-location set backups-secondary --default
```

Choose a location per backup:

```shell
velero backup create full-cluster-alternate-location-backup --storage-location backups-secondary
```

Both locations above use the credentials stored at install time in the `cloud-credentials` secret.

Limits:
- Each backup has exactly one BSL. You cannot send one backup to several locations; for redundancy create multiple schedules that differ only in storage location.
- File System Backup data lands under a prefix of the bucket of the BSL selected at creation.
- Velero does not encrypt metadata or volume data itself; it relies on the object and snapshot systems.
- Metadata compression is limited to Go's tar; fs-backup has no compression but does deduplicate.

## Checked

2026-11-08. Read in full: the Backup Storage Locations and Volume Snapshot Locations page. Every remaining claim was confirmed there. Removed or reworded: nothing.

Method: documentation only; no commands were run.
