---
id: computing-software.cloud-infrastructure-engineering.velero.fs-backup-opt-out
name: fs-backup-opt-out
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [default-volumes-to-fs-backup, backup-volumes-excludes, opt-out, fs-backup-exclude, volume-exclusion]
level: practitioner
status: docs-checked
description: "Back up all pod volumes with FSB by default and exclude some using backup.velero.io/backup-volumes-excludes."
sources:
  - https://velero.io/docs/main/file-system-backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In the opt-out approach every pod volume is backed up with FSB, except:
- volumes mounting the default service account token, Kubernetes Secrets and ConfigMaps
- hostPath volumes
- volumes you exclude explicitly with an annotation

Turn it on per backup with `--default-volumes-to-fs-backup`, or for all backups at install with `velero install --use-node-agent --default-volumes-to-fs-backup`.

Exclude volumes on each pod:

```bash
kubectl -n YOUR_POD_NAMESPACE annotate pod/YOUR_POD_NAME backup.velero.io/backup-volumes-excludes=YOUR_VOLUME_NAME_1,YOUR_VOLUME_NAME_2
```

Names are the volume names in the pod spec.

Important: an excluded volume is not simply skipped. Velero attempts to back it up with a volume snapshot instead, if CSI snapshots are enabled and the volume is CSI, or if a compatible VolumeSnapshotLocation is configured.

Check which method was used:

```bash
velero backup logs BACKUP_NAME | grep "skipped PVs"
velero backup describe BACKUP_NAME --details
kubectl -n velero get podvolumebackups -l velero.io/backup-name=BACKUP_NAME
```

A volume in the skipped PVs summary may still have been captured by snapshot. Look for the Velero-Native Snapshots or CSI Snapshots sections in the describe output.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/file-system-backup/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
