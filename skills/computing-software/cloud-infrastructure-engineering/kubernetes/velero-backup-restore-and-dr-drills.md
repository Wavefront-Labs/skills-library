---
id: computing-software.cloud-infrastructure-engineering.kubernetes.velero-backup-restore-and-dr-drills
name: velero-backup-restore-and-dr-drills
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, velero, backup, restore, disaster-recovery, csi-snapshot-data-movement, restic, kopia, node-agent, cross-cluster-restore, backupstoragelocation, schedule, dr-drill]
level: advanced
status: docs-checked
description: "Velero's actual backup mechanics for stateful workloads: CSI snapshots vs. file-system backup fallback, cross-cluster restore gotchas, and how to run a real DR drill."
sources: ["https://velero.io/docs/v1.18/csi/", "https://velero.io/docs/v1.18/csi-snapshot-data-movement/", "https://velero.io/docs/v1.18/file-system-backup/", "https://velero.io/docs/v1.18/restore-reference/", "https://velero.io/docs/v1.18/api-types/schedule/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Velero backup/restore — and why an untested backup is a hypothesis

**Goal:** know which of Velero's two very different volume-backup mechanisms is
actually running for a given PVC, and prove restore works before you need it for real.

## 1. Three backup paths, not one — know which is active
- **CSI snapshot** (needs the `EnableCSI` feature flag on the server: `--features=EnableCSI`): the Velero
  CSI plugins create a `VolumeSnapshot` (same CRDs as
  `computing-software.cloud-infrastructure-engineering.kubernetes.volume-snapshots-and-cloning`) that is
  retained for the lifetime of the backup. The data stays on the storage side.
- **CSI snapshot data movement** (opt-in per backup with `velero backup create NAME --snapshot-move-data`;
  `--data-mover` selects a data mover and the built-in one is the default): after the snapshot is taken,
  the data is moved to the backup storage location by data mover pods driven by `DataUpload` and
  `DataDownload` custom resources, and the snapshot is then removed. This makes backups portable across
  clusters and providers, not just a reference to a cloud-side snapshot that disappears if the source
  account or project is lost.
- **File System Backup (FSB, also called Pod Volume Backup)**: for volume types with no native snapshot
  concept (EFS, AzureFile, NFS, emptyDir, local) or when you prefer it, Velero reads the volume's files
  through the node's filesystem and backs them up to object storage with kopia (restic is deprecated;
  beta quality). Volumes are opted in per pod with the `backup.velero.io/backup-volumes` annotation or for
  all volumes with `--default-volumes-to-fs-backup`. Limits: `hostPath` volumes are unsupported, and only
  volumes mounted by a running pod can be backed up.

Check which path ran: look for `DataUpload` resources
(`kubectl -n velero get datauploads -l velero.io/backup-name=<name>`) for data movement, and
`PodVolumeBackup` resources for FSB; an empty expected set is the first sign backups aren't covering what you
think they are. `velero client config set features=EnableCSI` adds CSI object status to
`velero backup describe`.

## 2. BackupStorageLocation and reachability
Backups land in an object store (S3-compatible, Azure Blob, GCS) defined by a
`BackupStorageLocation`. The single most common "our backups were useless" incident:
the BSL is in the **same account/region/project** as the cluster it backs up —
account compromise or regional outage takes out both the cluster and its backups
simultaneously. For real disaster recovery, the BSL needs to be reachable from
outside the blast radius you're protecting against.

## 3. Cross-cluster / cross-account restore
```bash
velero restore create --from-backup <name> --namespace-mappings old-ns:new-ns
```
Restoring into a different cluster works for the Kubernetes objects and CSI
snapshot/data-mover volumes, but watch for:
- StorageClass names must exist in the target cluster, or be remapped with a ConfigMap in the `velero`
  namespace labelled `velero.io/plugin-config: ""` and `velero.io/change-storage-class: RestoreItemAction`
  whose data maps `<old-storage-class>: <new-storage-class>`. There is no restore flag for this.
- CSI driver identity: a plain CSI snapshot is tied to the originating driver and storage system, so it
  does not restore into a cluster on a different provider. CSI snapshot data movement exists for exactly
  this (the docs describe backing up from one cloud provider and restoring to another), and FSB data is
  also stored in the backup storage location.
- Data-mover and FSB backups restore onto whatever PVCs the target cluster provisions, which is why
  they matter for true DR even when plain CSI snapshots are faster day-to-day.

## 4. Scheduling and retention
```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata: {name: daily-prod}
spec:
  schedule: "0 3 * * *"
  template:
    includedNamespaces: [prod]
    ttl: 720h0m0s          # 30 days (the default if unset; server flag --default-backup-ttl)
```
`ttl` is per-backup retention, not a version history — Velero doesn't do
point-in-time granularity finer than how often the Schedule runs. For
application-consistent backups of a database, pair with
`computing-software.cloud-infrastructure-engineering.kubernetes.volume-snapshots-and-cloning`'s
guidance on quiescing or native DB backup tooling — a Velero snapshot inherits the
same crash-consistency limits as the underlying `VolumeSnapshot`.

## 5. The drill, not the backup, is the deliverable
A backup nobody has restored is a hypothesis, not a plan. A real DR drill:
1. Restore into a genuinely separate namespace or cluster (not the source).
2. Verify application-level correctness (query the restored database, not just
   "the pod started") — a restored PVC that mounts fine can still contain
   torn/inconsistent data from a crash-consistent snapshot.
3. Time it, and compare against the actual RTO the business expects — restore time
   for large volumes (data-mover download from object storage) can be the dominant
   factor compared with snapshot-only restores.
4. Re-run it periodically — a schema change, a new PVC that was never added to the
   backup's `includedNamespaces`/label selector, or an expired credential on the BSL
   are all things that silently break backups between drills.

## Gotchas
- A namespace or PVC that doesn't match the Schedule's `includedNamespaces` or label selectors is not
  backed up; review the selectors when new namespaces appear.
- FSB and data movement need the node-agent DaemonSet running on the nodes that host the relevant pods.
- Backups can end `Failed` or `PartiallyFailed`; check the phase and the per-volume status
  (`PodVolumeBackup` and `DataUpload` resources), not just whether the Schedule ran.

## Verify
- [ ] Knows, per PVC/StorageClass, which backup path (CSI snapshot data-mover vs.
      file-system backup) actually runs, not assumed.
- [ ] BackupStorageLocation is reachable independent of the primary cluster's
      account/region failing.
- [ ] Ran an actual restore into a separate namespace/cluster and verified
      application-level data correctness, within the last DR-drill cadence committed to.
- [ ] Checked `Phase: PartiallyFailed` history, not just `Completed` counts, over the
      last N scheduled backups.

## Checked

Checked on 2026-10-26 against the Velero v1.18 docs in `vmware-tanzu/velero` (`site/content/docs/v1.18`: csi, csi-snapshot-data-movement, file-system-backup, restore-reference, api-types/schedule; latest release v1.18.4, 2026-09-28).
Confirmed: `EnableCSI` flag, opt-in `--snapshot-move-data`, `--data-mover`, `DataUpload`/`DataDownload` CRs, FSB opt-in annotation and `--default-volumes-to-fs-backup`, restic deprecation, `hostPath` limitation, `--namespace-mappings`, the change-storage-class ConfigMap, Schedule `ttl` default of 30 days, `PartiallyFailed` backups.
Wrong in the draft: data movement is opt-in, not the default; `--storage-class-mappings` does not exist; the `describe --details` section names were unconfirmed; the volumeMode Block sentence was garbled and is removed. Removed as unconfirmed: silent node-agent skips.

Method: documentation only; no commands were run.
