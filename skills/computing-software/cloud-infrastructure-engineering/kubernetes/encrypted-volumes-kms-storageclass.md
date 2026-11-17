---
id: computing-software.cloud-infrastructure-engineering.kubernetes.encrypted-volumes-kms-storageclass
name: encrypted-volumes-kms-storageclass
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, storageclass, volume-encryption, kms, ebs-csi, csi]
level: practitioner
status: docs-checked
description: "Encrypt dynamically provisioned volumes with customer-managed KMS keys through StorageClass parameters on EBS, GCE PD and Azure Disk, including IAM and migration."
sources: ["https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/parameters.md", "https://github.com/kubernetes-sigs/aws-ebs-csi-driver/blob/master/docs/install.md", "https://github.com/kubernetes-sigs/gcp-compute-persistent-disk-csi-driver/blob/master/README.md", "https://github.com/kubernetes-sigs/azuredisk-csi-driver/blob/master/docs/driver-parameters.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypted volumes with KMS keys

## StorageClass per cloud
```yaml
# AWS EBS CSI
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
  kmsKeyId: arn:aws:kms:eu-west-1:111122223333:key/<key-id>
---
# GKE PD CSI
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-balanced
  disk-encryption-kms-key: projects/<p>/locations/<region>/keyRings/<ring>/cryptoKeys/<key>
---
# Azure Disk CSI
provisioner: disk.csi.azure.com
parameters:
  skuName: Premium_LRS
  diskEncryptionSetID: /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Compute/diskEncryptionSets/<des>
```
For EBS, `encrypted` defaults to `false`, `kmsKeyId` takes the full key ARN, and if `encrypted` is
true and no key is given AWS uses the region's default key (`/aws/ebs`). The GCE PD driver's
`disk-encryption-kms-key` parameter takes a fully qualified key identifier and encrypts new disks
with a customer-managed key. The Azure Disk driver's `diskEncryptionSetID` takes a disk encryption
set resource ID, and `diskEncryptionType` defaults to `EncryptionAtRestWithCustomerKey` when the
set is given.

## Permissions
- AWS: the EBS CSI driver documentation grants `kms:Decrypt`,
  `kms:GenerateDataKeyWithoutPlaintext` and `kms:CreateGrant` on the KMS keys used for
  encryption, and advises restricting the policy `Resource` to only the keys the driver needs.
- GKE and Azure: grant the key access that your provider's customer-managed-key documentation
  describes (see the provider links in the driver parameter docs); those pages are not
  reproduced here.

## Existing volumes
A PersistentVolume's backing disk is not re-encrypted by changing a StorageClass. The usual route
is to snapshot the volume, create a new PVC from the snapshot using the encrypted StorageClass,
switch the workload, then delete the old PVC; whether a snapshot of an unencrypted volume can be
restored into an encrypted one is provider-specific, so check your driver's snapshot
documentation first.

## Verify
```bash
kubectl get pv <pv> -o jsonpath='{.spec.csi.volumeHandle}'
```
Use the volume handle to look up the disk in your cloud's console or CLI and confirm the
encryption setting and key. Disable the key in a sandbox to learn what happens to new attaches
before relying on revocation.

## Checked

Checked 2026-10-27. Documentation checked: aws-ebs-csi-driver docs (parameters.md and install.md, master), gcp-compute-persistent-disk-csi-driver README (master), azuredisk-csi-driver driver-parameters.md (master). Confirmed: EBS `encrypted` and `kmsKeyId` parameters with their defaults, KMS actions in the driver install guide, GCE PD `disk-encryption-kms-key` parameter, Azure Disk `diskEncryptionSetID`, `diskEncryptionType` default and `skuName` values such as `Premium_LRS`. Removed as unconfirmed because the provider documentation is not in a readable repository: the GKE Compute Engine service agent role, the Azure Key Vault permission requirement, the claim that all three clouds encrypt by default with provider-managed keys, `kms:DescribeKey` as a required action (the driver guide lists three actions), the AWS CLI verification command and the "disabling the key must make attaches fail" assertion.

Method: documentation only; no commands were run.
