---
id: computing-software.cloud-infrastructure-engineering.rancher.rollback-rancher-with-backup-restore
name: rollback-rancher-with-backup-restore
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [rollback, restore, rancher-backup, rancher-cleanup, cleanup-sh, capi]
level: advanced
status: docs-checked
description: "Roll back Rancher after an upgrade by restoring a backup through a Restore resource, and when the rancher-cleanup scripts are needed first (v2.14.0 or later to v2.13.x)."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/install-upgrade-on-a-kubernetes-cluster/rollbacks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rolling back is only supported by restoring a backup taken before the upgrade, on the same upstream (local) cluster; changing versions with kubectl or Helm alone is not supported, and the target version must be under active support. Rancher must then be started at the lower version: after the restore, the page rolls the release back with `helm rollback rancher -n cattle-system` (`helm history rancher -n cattle-system` shows revisions; pass a revision number to pick one). The backup is applied by creating a `Restore` custom resource, either in the UI under the local cluster's **Rancher Backups > Restore**, or by `kubectl create -f restore.yaml`. The page's example Restore sets `backupFilename`, `encryptionConfigSecretName` and an `s3` `storageLocation` with credential secret, bucket, folder, region and endpoint.

Rancher is manually scaled down before the restore and scaled back up by the operator afterwards, so the UI is unavailable meanwhile; use the original cluster kubeconfig with the restore YAML. Resources are restored in order: CRDs, cluster-scoped resources, then namespaced resources.

**One special scenario needs extra steps:** rolling back from v2.14.0 or later to an earlier v2.13.x. The embedded cluster-api was removed in v2.14.0 and Rancher Turtles became the only supported CAPI manager, and cluster-api CRDs move from `cluster.x-k8s.io/v1beta1` to `v1beta2`, so restoring v2.13.x backup data fails at first.

For this case, first run the `cleanup.sh` and `verify.sh` scripts from the rancher/rancher-cleanup repository on the upstream cluster. `cleanup.sh` deletes resources Rancher created, so expect downtime. Then follow the migrate-to-a-new-cluster procedure, skipping the cert-manager step if it still exists and installing the Rancher version you are rolling back to.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Rollbacks. Fixed: the page now lists only the v2.14.0 to v2.13.x special scenario, so the v2.6.4 and v2.7.7 scenarios were removed; added the documented helm rollback step and the note that Helm/kubectl version changes alone are unsupported.

Method: documentation only; no commands were run.
