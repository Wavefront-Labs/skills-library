---
id: computing-software.cloud-infrastructure-engineering.longhorn.system-restore
name: system-restore
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [system-restore, systemrestore, rollout, detached-volumes, troubleshooting]
level: advanced
status: docs-checked
description: "Restore a Longhorn system backup with the SystemRestore CRD: prerequisites, what is and is not restored, deletion warning and hang troubleshooting."
sources:
  - https://longhorn.io/docs/1.13.0/advanced-resources/system-backup-restore/restore-longhorn-system/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: roll a system backup into a running Longhorn cluster.

Prerequisites: a running Longhorn cluster, node and disk tags set up for the StorageClass, an existing system backup, and all existing volumes detached.

Create a `SystemRestore` (`longhorn.io/v1beta2`, namespace `longhorn-system`) whose `spec.systemBackup` names the backup.

```bash
kubectl -n longhorn-system get systembackup
# apply a SystemRestore manifest referencing it, then
kubectl -n longhorn-system get systemrestore
```

Wait for `Completed`. UI: Backup and Restore, System Backups, select, Restore from the Operation menu, name it.

Rollout:
- Restores resources from the system backup bundle.
- Does not restore existing Volumes, PVs or PVCs.
- Restores each Volume from its latest backup.
- Skips `ConfigMap/longhorn-default-setting` and configurable settings (including the concurrent volume backup restore and concurrent replica rebuild per node limits).
- V2 backing images are not backed up, so they must already exist.

Deleting a SystemRestore also deletes the associated job and aborts the remaining rollouts. To restart, delete the in-progress restore and create a new one: `kubectl -n longhorn-system delete systemrestore/<name>`.

Restore across major or minor versions is not supported, except for upgrade failures.

If it hangs, read the rollout job logs and fix the problem resource, then restart:

```bash
kubectl -n longhorn-system logs --selector=job-name=longhorn-system-rollout-<SYSTEM-RESTORE-NAME>
```

## Checked

2026-11-08. Read in full against https://longhorn.io/docs/1.13.0/advanced-resources/system-backup-restore/restore-longhorn-system/ : prerequisites, rollout behaviour, excluded settings, delete and restart behaviour, troubleshooting command. Nothing else was removed.

Method: documentation only; no commands were run.
