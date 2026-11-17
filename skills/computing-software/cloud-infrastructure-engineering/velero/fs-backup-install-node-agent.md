---
id: computing-software.cloud-infrastructure-engineering.velero.fs-backup-install-node-agent
name: fs-backup-install-node-agent
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [file-system-backup, node-agent, use-node-agent, kopia, pod-volume-backup]
level: practitioner
status: docs-checked
description: "Enable File System Backup with velero install --use-node-agent, what repositories it creates per namespace, and how it relates to snapshots."
sources:
  - https://velero.io/docs/main/file-system-backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
File System Backup (FSB, also Pod Volume Backup) copies volume data from the live file system using the Kopia modules. It is beta quality. It can back up almost any volume type (EFS, AzureFile, NFS, emptyDir, local) and is not tied to a storage platform, but data is captured from a live file system so it is less consistent than a snapshot, and node-agent pods must run as root, sometimes privileged.

Install the node agent, a DaemonSet that hosts the FSB controllers:

```
velero install --use-node-agent
```

Add `--use-volume-snapshots=false` when your storage has no snapshot support, so no unused VolumeSnapshotLocation is created. Requires Kubernetes 1.16 or later and MountPropagation. FSB supports object storage only; a non-listed backend must be S3 compatible with correct bucket and endpoint in the BackupStorageLocation.

Velero creates one backup repository per namespace, for example `https://s3-us-west-2.amazonaws.com/bucket/kopia/ns1`. Inspect them with `velero repo get`.

FSB and volume snapshots are mutually exclusive per volume: a volume backed up by FSB is not snapshotted, and a volume opted out of FSB is snapshotted if snapshots are configured. hostPath volumes are not supported; local volumes are.

Troubleshoot with `kubectl -n velero get podvolumebackups -l velero.io/backup-name=NAME -o yaml`.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/file-system-backup/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
