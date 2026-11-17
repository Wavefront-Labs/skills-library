---
id: computing-software.cloud-infrastructure-engineering.rancher.backup-storage-location-s3-or-pvc
name: backup-storage-location-s3-or-pvc
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [rancher-backup, s3, storageclass, persistent-volume, reclaim-policy, minio]
level: practitioner
status: docs-checked
description: "Configure where Rancher backups are stored: no default, an S3-compatible bucket with credentials and endpoint CA, or a StorageClass PVC, and why the reclaim policy must be Retain."
sources:
  - https://ranchermanager.docs.rancher.com/reference-guides/backup-restore-configuration/storage-configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Only **one** storage location can be set at operator level, and each individual backup may override it, but only with an S3-compatible object store.

Options:

- **No default.** Every Backup must then specify an S3-compatible store.
- **S3-compatible object store.** Parameters: a Credential Secret chosen from Rancher secrets, Bucket Name (default `rancherbackups`), Region, Folder (empty means the bucket root), Endpoint (for example `s3.us-west-2.amazonaws.com`), Endpoint CA, and `insecureTLSSkipVerify`, which is set to true if you are not using TLS.
- **Existing StorageClass.** Installing the `rancher-backup` chart with this option creates a PVC and Kubernetes dynamically provisions a PV to hold the backups.

For the StorageClass path the page strongly recommends a StorageClass (or Persistent Volume) with a reclaim policy of **Retain**. Otherwise, if the PVC created by the chart is deleted, whether during an app upgrade or by accident, the PV is deleted too, and every backup stored in it goes with it.

For S3 restores that need credentials, the secret data must contain the two keys `accessKey` and `secretKey`; it can live in any namespace, and `credentialSecretNamespace` tells the app where to look.

For chart-level configuration through the Helm CLI, the page points to the documented `values.yaml` in the backup-restore-operator repository rather than listing every value.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Backup Storage Location Configuration; Backup Configuration. Nothing removed.

Method: documentation only; no commands were run.
