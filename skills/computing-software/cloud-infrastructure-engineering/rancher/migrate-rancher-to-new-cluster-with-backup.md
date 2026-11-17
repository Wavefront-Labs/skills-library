---
id: computing-software.cloud-infrastructure-engineering.rancher.migrate-rancher-to-new-cluster-with-backup
name: migrate-rancher-to-new-cluster-with-backup
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [migration, rancher-backup, restore, prune-false, hostname, local-cluster, k3s-to-rke2]
level: advanced
status: docs-checked
description: "Move Rancher to a new cluster: install rancher-backup first, restore with prune false, edit the local cluster object across distributions, then install cert-manager and Rancher."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/backup-restore-and-disaster-recovery/migrate-rancher-to-new-cluster
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Do **not** install Rancher on the new cluster first; restoring into a cluster that already has Rancher can cause problems. The backup covers only Rancher resources and can move them between any two Kubernetes clusters (Rancher v2.5.0 or newer). You **must reuse the original server URL hostname**; otherwise downstream clusters show as unavailable and you cannot open them.

Sequence:

1. Install `rancher-backup-crd` and `rancher-backup` from the `rancher-charts` repo into `cattle-resources-system`, picking a chart version listed as compatible in the support matrix. For air gaps set `image.repository` and `global.kubectl.repository` to your registry; if the Helm host is also offline, `helm fetch` both charts elsewhere and install from the tarballs.
2. For S3 sources create a secret with keys `accessKey` and `secretKey`, then apply a `Restore` with **`prune: false`** (required during migration) and `encryptionConfigSecretName` only if the backup was encrypted. If you only hold the config file, recreate the secret in `cattle-resources-system`. Watch with `kubectl get restore` and the `rancher-backup` pod logs until status is `Completed`.
3. Install cert-manager.
4. Install Rancher with Helm using the same Helm version, the original hostname and `--version` set.

Moving between distributions (for example K3s to RKE2): after the restore and **before** starting Rancher, run `kubectl edit clusters.management.cattle.io local`. Set `status.driver` to `imported`; remove `status.provider`, the whole `status.version` map, the `provider.cattle.io` label, the `management.cattle.io/current-cluster-controllers-version` annotation, and `spec.rke2Config` or `spec.k3sConfig`. Removing those erases the local cluster's distribution-specific upgrade configuration.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Migrating Rancher to a New Cluster. Nothing removed.

Method: documentation only; no commands were run.
