---
id: computing-software.cloud-infrastructure-engineering.velero.fs-backup-opt-in
name: fs-backup-opt-in
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [backup-volumes, opt-in, fs-backup-annotation, podvolumebackups, pod-annotation]
level: practitioner
status: docs-checked
description: "Select pod volumes for File System Backup with the backup.velero.io/backup-volumes annotation, the default opt-in approach."
sources:
  - https://velero.io/docs/main/file-system-backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Opt-in is the default way Velero discovers volumes for FSB. Annotate each pod with the names of the volumes (names from the pod spec) to back up:

```bash
kubectl -n YOUR_POD_NAMESPACE annotate pod/YOUR_POD_NAME backup.velero.io/backup-volumes=YOUR_VOLUME_NAME_1,YOUR_VOLUME_NAME_2
```

Example: `kubectl -n foo annotate pod/sample backup.velero.io/backup-volumes=pvc-volume,emptydir-volume`. If a controller manages the pods, put the annotation in the pod template spec so recreated pods keep it.

Then back up and inspect:

```bash
velero backup create NAME OPTIONS...
velero backup describe YOUR_BACKUP_NAME
kubectl -n velero get podvolumebackups -l velero.io/backup-name=YOUR_BACKUP_NAME -o yaml
```

Volumes that are not annotated are still considered for snapshots when all hold: `--snapshot-volumes` is not `false`, the volume supports snapshots (CSI or native), and either CSI snapshots are enabled for a CSI volume or a compatible VolumeSnapshotLocation exists.

Decision order for each volume: opted out of FSB means snapshot if configured; opted in (annotation or `--default-volumes-to-fs-backup`) means FSB and no snapshot; otherwise snapshot if configured.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/file-system-backup/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
