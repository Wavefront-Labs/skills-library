---
id: computing-software.cloud-infrastructure-engineering.longhorn.create-backup
name: create-backup
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [backup, incremental, backup-crd, full-backup, labels]
level: intro
status: docs-checked
description: "Create a Longhorn backup from the UI or a Backup CR with backupMode incremental, and how incremental and full backups behave."
sources:
  - https://longhorn.io/docs/1.13.0/snapshots-and-backups/backup-and-restore/create-a-backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: back up a volume to the backup target.

Prerequisite: a backup target must be configured, otherwise creating a backup errors.

UI: Volume menu, select the volume, Create Backup, add labels, OK. The backup appears under Backup in the top bar.

kubectl: get the snapshot name from the UI or CR, then apply:

```yaml
apiVersion: longhorn.io/v1beta2
kind: Backup
metadata:
  name: backup-example
  namespace: longhorn-system
spec:
  backupMode: incremental
  snapshotName: snapshot-name-example
  labels:
    app: test
```

Behaviour:
- By default only data changed since the last backup is uploaded (delta backup).
- Corrupted blocks in the backupstore are not replaced by later incremental backups.
- Full backups (v1.7.0+) upload all data blocks and overwrite existing ones in the backupstore.

Backups use compressed 2 MB blocks, so a changed 4K block backs up the whole block, and an empty incremental backup shows 0 bytes yet restores full data. Schedule backups with recurring jobs.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/snapshots-and-backups/backup-and-restore/create-a-backup/

No claim needed changing.

Method: documentation only; no commands were run.
