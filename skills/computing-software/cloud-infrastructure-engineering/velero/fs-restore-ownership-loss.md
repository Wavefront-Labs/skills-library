---
id: computing-software.cloud-infrastructure-engineering.velero.fs-restore-ownership-loss
name: fs-restore-ownership-loss
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [chown, mount-constant-identity, azure-files, gcsfuse, root-squash]
level: sme
status: docs-checked
description: "Diagnose silent ownership loss after FSB restore on SMB, blobfuse, gcsfuse and root-squashed NFS, and the Azure Files remediation."
sources:
  - https://velero.io/docs/main/file-system-backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Some volumes fix ownership and mode by mount configuration. On them FSB restore chown/chmod as root returns success while changing nothing, so the restore reports `Completed` with no warnings and no log hint.

Affected: Azure Files SMB with default or forced `uid=`/`gid=` mounts (chown is a silent no-op, chmod forced by `file_mode=`/`dir_mode=`); Azure Blob via blobfuse2 (both no-ops); GCP Cloud Storage FUSE (`gcsfuse.csi.storage.gke.io`); AWS FSx for Windows (NTFS ACLs do not map); EFS Access Points with a `PosixUser`.

Works with real POSIX: Azure Disk, plain Azure Files or EFS, Azure Files NFS 4.1 Premium, Azure Blob NFSv3 Premium.

Remediation for Azure Files SMB: add `idsfromsid,modefromsid` to the StorageClass `mountOptions` and do not force `uid=`, `gid=` or mode with them. Non-root workloads may need a one-time root init container to chown the volume root. No remediation exists for blobfuse or gcsfuse.

NFS `root_squash` returns a real `EPERM`, but Kopia integration sets `IgnorePermissionErrors: true`, which discards it, giving the same symptom.

Diagnose with `mount | grep -E 'cifs|fuse|nfs'`. Signature: clean restore, then the app fails, for example PostgreSQL reporting wrong ownership of its data directory.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/file-system-backup/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
