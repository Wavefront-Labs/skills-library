---
id: computing-software.cloud-infrastructure-engineering.velero.object-storage-sync
name: object-storage-sync
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [object-storage-sync, source-of-truth, cluster-migration, backup-sync, bsl]
level: practitioner
status: docs-checked
description: "How Velero treats object storage as the source of truth, syncing backups into a new cluster and removing Completed backups whose tarball is gone."
sources:
  - https://velero.io/docs/main/how-velero-works/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Velero treats object storage as the source of truth and continuously checks that the right backup resources exist.

Sync into the cluster: if a properly formatted backup file sits in the bucket but no `Backup` resource exists in the Kubernetes API, Velero creates the resource from the bucket contents. This lets restore work in a cluster migration scenario, where the original backup objects do not exist in the new cluster.

Sync out of the cluster: if a `Completed` backup object exists in Kubernetes but its tarball is gone from object storage, Velero deletes the object from Kubernetes. Backups in `Failed` or `PartiallyFailed` phase are never removed by this sync.

Practical consequences:
- Removing a Completed backup's tarball from the bucket by hand makes Velero delete the matching backup object from the cluster.

## Checked

2026-11-08. Read in full: the How Velero Works page. Every remaining claim was confirmed there. Removed or reworded: the step-by-step migration recipe and the versioning/access-control advice.

Method: documentation only; no commands were run.
