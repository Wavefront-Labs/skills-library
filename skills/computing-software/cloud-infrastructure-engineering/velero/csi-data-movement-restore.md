---
id: computing-software.cloud-infrastructure-engineering.velero.csi-data-movement-restore
name: csi-data-movement-restore
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [datadownload, restore-data-movement, existing-volume-data-policy, storage-class-target, restore-create]
level: practitioner
status: docs-checked
description: "Restore data-moved volumes: DataDownload monitoring, target cluster storage class handling and --existing-volume-data-policy."
sources:
  - https://velero.io/docs/main/csi-snapshot-data-movement/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
No mover settings are needed at restore; Velero reads them from the backup metadata:

```bash
velero restore create --from-backup BACKUP_NAME
kubectl -n velero get datadownloads -l velero.io/restore-name=RESTORE_NAME -w
velero restore describe RESTORE_NAME --details
```

Each volume produces a `DataDownload`, ending `Completed`, `Failed` or `Cancelled`. `status.activities` and `status.message` explain details and failures.

Target cluster storage class: built-in data movement creates a PVC with the same spec as the source and expects it to provision the same way, so CSI features are not required on the target but the storage class must work. Storage classes are cluster scoped and not restored by default, unless `--include-cluster-resources` is given. Best practice: create a working class with the same name as the source; the restore then skips the backed-up one. If the name differs, use the change-storage-class ConfigMap or skip restoring storage classes.

Restore into an existing bound PVC with `--existing-volume-data-policy=full` or `incremental`. First stop consuming workloads, for example scale Deployments and StatefulSets to zero and wait until their pods have terminated.

The file system mover shares the ownership loss problem on mount-constant-identity volumes, and repositories use a static encryption key.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/csi-snapshot-data-movement/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
