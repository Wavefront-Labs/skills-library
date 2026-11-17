---
id: computing-software.cloud-infrastructure-engineering.rancher.rancher-backup-operator-install-and-backup
name: rancher-backup-operator-install-and-backup
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [rancher-backup, backup-restore-operator, backup, local-cluster, s3]
level: practitioner
status: docs-checked
description: "Install the Rancher Backups app on the local cluster and create a Backup resource: resourceSetName, schedule, retentionCount, encryption."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/backup-restore-and-disaster-recovery/back-up-rancher
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The backup-restore operator is installed in the **local** cluster (the one running Rancher), only backs up the Rancher app, and only operates on the local cluster. Rancher must be v2.5.0 or newer. Backups are `.tar.gz` files that can go to S3 or Minio, or onto a persistent volume. When restoring into a new Rancher setup, use the same Rancher version as the one that was backed up; the Kubernetes apiVersions in the cluster and the backup file also matter.

Install it from the UI: **Cluster Management**, the `local` cluster, **Explore**, **Apps > Charts > Rancher Backups > Install**. The default storage location is an operator-level setting, so it is chosen at install or upgrade time.

Then create a `Backup` custom resource under **Rancher Backups > Backups** (form or **Create from YAML**). The page's example is an encrypted recurring S3 backup:

```yaml
apiVersion: resources.cattle.io/v1
kind: Backup
metadata:
  name: s3-recurring-backup
spec:
  storageLocation:
    s3:
      credentialSecretName: s3-creds
      credentialSecretNamespace: default
      bucketName: rancher-backups
      folder: rancher
      region: us-west-2
      endpoint: s3.us-west-2.amazonaws.com
  resourceSetName: rancher-resource-set-full
  encryptionConfigSecretName: encryptionconfig
  schedule: "@every 1h"
  retentionCount: 10
```

In YAML, `resourceSetName` must be `rancher-resource-set-full` or `rancher-resource-set-basic`. The operator does not save the EncryptionConfiguration file: keep its contents, because the same file is needed to restore. A known Fleet issue after restores concerns `clientSecretName` and `helmSecretName` secrets not being included in gitrepos; the page links a workaround in the Fleet troubleshooting section.

## Checked

2026-11-09. Read the cited Backing up Rancher page in full and checked every claim against it (local cluster scope, v2.5.0 prerequisite, install path, Backup example, resourceSetName values, EncryptionConfiguration warning, Fleet issue). Trimmed the cattle-resources-system tag, which the page does not mention.

Method: documentation only; no commands were run.
