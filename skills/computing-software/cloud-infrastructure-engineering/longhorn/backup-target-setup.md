---
id: computing-software.cloud-infrastructure-engineering.longhorn.backup-target-setup
name: backup-target-setup
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [backup-target, s3, nfs, cifs, azure-blob]
level: practitioner
status: docs-checked
description: "Configure Longhorn backup targets for S3, NFS, SMB/CIFS and Azure Blob: URL formats, credential secret keys, Helm defaults and proxy or certificate options."
sources:
  - https://longhorn.io/docs/1.13.0/snapshots-and-backups/backup-and-restore/set-backup-target/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: point Longhorn at a backupstore.

Configure under Settings, Backup Target, or Backup and Restore, Backup Targets. Since v1.8.0 multiple targets are supported; the default is named `default`. Do not apply retention policies directly on the backupstore.

Defaults: Helm `defaultBackupStore.backupTarget`, `.backupTargetCredentialSecret`, `.pollInterval`; or ConfigMap `longhorn-default-resource` with keys `backup-target`, `backup-target-credential-secret`, `backupstore-poll-interval`.

URL and secret keys (secrets live in `longhorn-system`):
- S3: `s3://<bucket>@<region>/` (trailing `/` required); `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` or `AWS_IAM_ROLE_ARN`
- NFS: `nfs://<server>:<path>` (NFSv4); no secret
- SMB/CIFS: `cifs://<host>/<path>`; `CIFS_USERNAME`, `CIFS_PASSWORD`
- Azure: `azblob://<container>@core.windows.net/`; `AZBLOB_ACCOUNT_NAME`, `AZBLOB_ACCOUNT_KEY`

S3 extras: `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` (must include `localhost`, `127.0.0.1`, `0.0.0.0`, `10.0.0.0/8`, `192.168.0.0/16`); `AWS_CERT` in PEM for self-signed CAs; `VIRTUAL_HOSTED_STYLE=true`.

NFS default mount options `actimeo=1,soft,timeo=300,retry=2`; custom `nfsOptions` have `hard` removed and `soft` added. CIFS default is `soft`; custom `cifsOptions` replaces defaults.

When base64-encoding secret values use `echo -n`. Errors show as toasts; inspect `/v1/backuptargets` for detail.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/snapshots-and-backups/backup-and-restore/set-backup-target/

No claim needed changing.

Method: documentation only; no commands were run.
