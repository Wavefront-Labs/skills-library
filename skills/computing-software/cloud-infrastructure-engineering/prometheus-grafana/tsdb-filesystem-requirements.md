---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.tsdb-filesystem-requirements
name: tsdb-filesystem-requirements
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [tsdb-filesystem-requirements, prometheus-nfs, tsdb, storage, kubernetes-storage, persistent-volume]
level: practitioner
status: docs-checked
description: "Choose storage for the Prometheus TSDB: POSIX local filesystems, why NFS and EFS are unsupported, and the Operator's PVC, fsGroup and resize steps."
sources: ["https://prometheus.io/docs/prometheus/latest/storage/#operational-aspects", "https://prometheus-operator.dev/docs/platform/storage/", "https://prometheus.io/docs/introduction/faq/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TSDB filesystem requirements

Prometheus docs: non-POSIX compliant filesystems are not supported for local storage because unrecoverable corruption may happen. NFS filesystems (including AWS's EFS) are not supported: NFS could be POSIX-compliant, but most implementations are not. Use a local filesystem. Local storage is also not clustered or replicated, so it is not arbitrarily scalable or durable through drive or node outages and should be managed like any single-node database. Use snapshots for backups.

## Prometheus Operator
By default the Operator stores data on `emptyDir` volumes, which are not persisted when Pods are redeployed. For persistence set `spec.storage.volumeClaimTemplate` on the Prometheus resource; a PersistentVolumeClaim is created for each Pod in the StatefulSet, and the storage should be provisioned automatically when the cluster has a StorageClass with dynamic provisioning.
```yaml
spec:
  storage:
    volumeClaimTemplate:
      spec:
        storageClassName: ssd
        resources:
          requests:
            storage: 40Gi
```
The Operator docs advise volumes with high I/O throughput. For a volume that cannot be provisioned dynamically, use a `selector` with `matchLabels` in the claim template alongside a manually created PersistentVolume with `ReadWriteOnce` access (marked required in their example).
The Operator storage page shows an NFS-backed PersistentVolume as an example of manual provisioning; that conflicts with the Prometheus guidance above, so do not use NFS for the TSDB.

## Volume permissions
The Prometheus container runs as a non-root user (nobody, UID 65534 in the default image) and the Operator sets no Pod security context unless you configure one. If the volume root is owned by root and not writable by others, Prometheus fails to start and the Pod crash-loops. Set `fsGroup` in `spec.securityContext`:
```yaml
spec:
  securityContext:
    fsGroup: 65534
    runAsNonRoot: true
    runAsUser: 65534
```
Whether `fsGroup` takes effect depends on the volume type and, for CSI volumes, the driver's `fsGroupPolicy`; when it does not, make the directory writable on the storage side. For `hostPath` volumes the container must have permission to the host path.

## Resizing
Kubernetes does not support volume expansion through StatefulSets, so changing `spec.storage` makes the Operator delete and recreate the StatefulSet and the PVCs are not expanded. Manual fix from the Operator docs:
1. Check the StorageClass has `allowVolumeExpansion: true`.
2. Set `spec.paused: true` on the Prometheus resource and update the storage request in `spec.storage`.
3. Patch every PVC (selected by `operator.prometheus.io/name=<name>`) with the new request.
4. Delete the StatefulSet with `--cascade=orphan`.
5. Set `spec.paused: false`; the Operator recreates the StatefulSet without service disruption.

## Checked
Date: 2026-11-07.
Read in full: Prometheus Storage page (filesystem caution, not clustered, snapshots), the Prometheus Operator Storage page (emptyDir default, `volumeClaimTemplate`, manual provisioning, volume permissions, hostPath, resizing procedure) and the Prometheus FAQ (it has no storage-filesystem content).
Removed because no cited page confirms them: ext4/xfs and cloud disk product advice, the claims about Azure Files, SMB, s3fs and gcsfuse, `noatime`, IOPS and throughput figures, the `--storage.tsdb.no-lockfile` and Operator statement, the snapshot crash-consistency claim, `df -T` and alert Verify steps, and the `gp3` example (replaced with the Operator page's `ssd` example).
Method: documentation only; no commands were run.
