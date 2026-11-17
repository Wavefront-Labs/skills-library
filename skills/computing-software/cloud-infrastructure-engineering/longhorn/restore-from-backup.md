---
id: computing-software.cloud-infrastructure-engineering.longhorn.restore-from-backup
name: restore-from-backup
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [restore, from-backup, volume-cr, pv, pvc]
level: practitioner
status: docs-checked
description: "Restore a Longhorn backup into a volume via the UI or Volume CR with fromBackup, exact byte sizing, and manual PV and PVC binding."
sources:
  - https://longhorn.io/docs/1.13.0/snapshots-and-backups/backup-and-restore/restore-from-a-backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bring a backup back as a usable volume.

UI: Backup, select backup(s), Restore Latest Backup, choose the new volume Name, OK. Then create the PV/PVC; leave `storageClassName` empty to inherit the backup volume's PVC StorageClass, or set an existing one. By default the volume takes the backup's name; if a volume with that name exists, nothing is restored.

CLI:
1. `kubectl get backups.longhorn.io -n longhorn-system`
2. Read `url` and `volumeSize` (bytes) from the Backup CR `status`.
3. Create a `Volume` (`longhorn.io/v1beta2`, `longhorn-system`) with:
   - `size`: the exact byte count as a quoted string (quantities like `1Gi` or unquoted integers cause an admission webhook error)
   - `fromBackup`: the backup `url`
   - `numberOfReplicas: 3`, `frontend: blockdev`, `dataEngine: v1`
4. Wait until the volume is `detached` with `status.restoreRequired` false.
5. Bind manually: a PV with `csi.driver: driver.longhorn.io`, `volumeHandle` equal to the Volume CR name, `storageClassName: longhorn`, `ReadWriteOnce` and matching capacity; then a PVC whose `volumeName` points at the PV with the same storage class and access mode.

The PVC is then bound to the restored volume and ready for workloads. The StorageClass Parameters reference lists `fromBackup` as the URL of a backup to be restored from.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/snapshots-and-backups/backup-and-restore/restore-from-a-backup/

Changed: the StorageClass fromBackup remark now cites the StorageClass Parameters reference wording, which the restore page does not contain.

Method: documentation only; no commands were run.
