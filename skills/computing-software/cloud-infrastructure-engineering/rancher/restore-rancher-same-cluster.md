---
id: computing-software.cloud-infrastructure-engineering.rancher.restore-rancher-same-cluster
name: restore-rancher-same-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [restore, rancher-backup, prune, encryptionconfigsecretname, backupfilename, fleet]
level: practitioner
status: docs-checked
description: "Restore Rancher on the same local cluster at the same version: Restore resource fields, prune and deleteTimeoutSeconds, getting the S3 backupFilename right, and Fleet caveats."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/backup-restore-and-disaster-recovery/restore-rancher
  - https://ranchermanager.docs.rancher.com/reference-guides/backup-restore-configuration/restore-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use this page when Rancher is at the same version as when the backup was taken and the upstream (local) cluster is the same one. For a new cluster use the migration procedure; for a previous version after an upgrade use rollback.

When the restore starts, the operator scales the Rancher deployment down and scales it back up afterwards, so **Rancher is unavailable during the restore**. Fleet users must also think about Kubernetes API server availability and paused GitRepos; the page links the Fleet documentation on backing up and restoring.

Create a `Restore` under the local cluster's **Rancher Backups > Restores**. The core fields are `backupFilename`, `storageLocation` (omit to use the default target, or give S3 details), `encryptionConfigSecretName` and `prune`.

- **Backup source:** an existing Backup resource, the default storage target, or an S3-compatible store. Without a Backup resource you need the exact filename.
- **S3 filename:** relative to the configured folder. With base folder `s3folder` and a file in subfolder `s3sub`, use `s3sub/backupfile`.
- **Encryption:** if the file ends `.enc`, supply the secret from `cattle-resources-system` with identical contents to the one used for the backup, or the restore fails.
- **Prune:** enabled by default and recommended; it deletes Rancher-managed resources created after the backup so the state matches exactly. `deleteTimeoutSeconds` is how long the operator waits on a delete before removing finalizers and retrying.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Restoring Rancher; Restore Configuration. Nothing removed.

Method: documentation only; no commands were run.
