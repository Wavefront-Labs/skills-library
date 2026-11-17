---
id: computing-software.cloud-infrastructure-engineering.kubernetes.readwritemany-storage-nfs-efs-cephfs
name: readwritemany-storage-nfs-efs-cephfs
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, readwritemany-options, nfs, nfs-csi, nfs-subdir, efs-csi, cephfs, azure-files, filestore, shared-storage]
level: practitioner
status: docs-checked
description: "Provide ReadWriteMany volumes: pick between NFS CSI, EFS, Azure Files, Filestore and CephFS, install the NFS CSI driver, and avoid the performance, permission and locking traps."
sources: ["https://github.com/kubernetes-csi/csi-driver-nfs/blob/master/docs/driver-parameters.md", "https://github.com/kubernetes-csi/csi-driver-nfs/blob/master/charts/README.md", "https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/docs/parameters.md", "https://github.com/kubernetes-sigs/azurefile-csi-driver/blob/master/docs/driver-parameters.md", "https://github.com/kubernetes-sigs/gcp-filestore-csi-driver", "https://github.com/rook/rook/blob/master/Documentation/Storage-Configuration/Shared-Filesystem-CephFS/filesystem-storage.md", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ReadWriteMany storage: NFS, EFS, CephFS and friends

Block volumes (EBS, PD, Azure Disk) are normally mounted by one node at a time (`ReadWriteOnce`). When
several pods on different nodes must share a filesystem (CMS uploads, ML datasets, legacy apps), you
need a network filesystem that supports `ReadWriteMany`. First ask whether object storage
(S3/GCS) would do; it is usually simpler.

## Options
| Backend | Driver | Notes |
|---|---|---|
| Existing NFS server/NAS | `nfs.csi.k8s.io` (csi-driver-nfs) | dynamic provisioning creates a subdirectory per PVC; the NFS server itself must already exist and be configured (NFSv3 or NFSv4); availability is the server's problem |
| AWS EFS | `efs.csi.aws.com` | dynamic provisioning through EFS access points (`provisioningMode: efs-ap`) with POSIX `uid`/`gid` per access point; also static provisioning; mounted with encryption in transit by default on the driver's master branch |
| Azure Files | `file.csi.azure.com` | `protocol` parameter selects `smb` (default) or `nfs` |
| GCP Filestore | Filestore CSI driver | `tier` parameter (standard, premium, enterprise, high-scale and others); check the driver README for the capacity limits of each tier |
| CephFS (Rook) | `<operator-namespace>.cephfs.csi.ceph.com`, for example `rook-ceph.cephfs.csi.ceph.com` | self-hosted; needs a running Ceph cluster and Ceph operations skills |
`nfs-subdir-external-provisioner` (kubernetes-sigs) is a separate, older provisioner that creates
subdirectories on an NFS export; prefer csi-driver-nfs for new setups.

## NFS CSI driver
```bash
helm repo add csi-driver-nfs https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/charts
helm search repo csi-driver-nfs --versions
helm install csi-driver-nfs csi-driver-nfs/csi-driver-nfs -n kube-system --version <chart-version>
```
Pick `<chart-version>` from the `helm search` output (the project's chart README shows its own
current example); the project also documents an alternative repo URL,
`https://kubernetes-csi.github.io/csi-driver-nfs`.
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: {name: nfs-shared}
provisioner: nfs.csi.k8s.io
parameters:
  server: nas.internal
  share: /export/k8s
  subDir: ${pvc.metadata.namespace}-${pvc.metadata.name}
  onDelete: retain          # delete (default), retain or archive
reclaimPolicy: Retain
mountOptions: [nfsvers=4.1, hard, noatime]
allowVolumeExpansion: true
```
`subDir` supports `${pvc.metadata.name}` and `${pvc.metadata.namespace}` substitution, and the driver
creates the directory if it does not exist. Nodes need NFS client packages (`nfs-common` /
`nfs-utils`).

## Traps
- **Permissions**: the csi-driver-nfs documentation lists `fsGroup` handling (the driver advertises
  `fsGroupPolicy: File`, and the NFS export must allow the kubelet's `chown`/`chgrp` on the mount
  root, for example `no_root_squash`; root-squashed exports can fail the mount) and, as a last
  resort, the `mountPermissions` parameter (`0777` makes the share world-writable and is unsuitable
  across trust boundaries). With EFS dynamic provisioning set `uid`/`gid` (or `gidRangeStart`) so
  access points get the POSIX identity your pods run as.
- **Databases**: do not put a database on a shared network filesystem unless the database vendor
  documents support for it.
- **Capacity**: `requests.storage` on a network share is a request to the driver, not necessarily
  an enforced quota; confirm quota behaviour for your backend.
- **Performance**: small-file and metadata-heavy workloads depend heavily on the backend and mount
  options; measure with your own workload.

## Verify
- [ ] Two pods on different nodes write and read the same file; PVC deletion behaviour matches
      `reclaimPolicy` and `onDelete`.
- [ ] A throughput and metadata test with your real workload meets the application's need.

## Checked

Checked 2026-10-27. Documentation checked: csi-driver-nfs docs (driver-parameters.md and chart README, master), aws-efs-csi-driver docs (README, parameters.md, install.md, master), azurefile-csi-driver driver-parameters.md (master), gcp-filestore-csi-driver README (master), Rook CephFS storage configuration page (master), nfs-subdir-external-provisioner README (master). Confirmed: `nfs.csi.k8s.io` parameters `server`, `share`, `subDir` (with `${pvc.metadata.name}`/`${pvc.metadata.namespace}`), `onDelete`, `mountPermissions` and the fsGroup and no_root_squash notes; EFS access-point provisioning parameters; Azure Files `protocol` values; Filestore `tier` values; Rook `rook-ceph.cephfs.csi.ceph.com` provisioner with an operator-namespace prefix. Fixed: the pinned Helm chart version `v4.9.0` (not the documented form; the chart README uses versions without a leading `v`, for example 4.13.6, and says to choose from `helm search repo`). Removed as unconfirmed: the Filestore 1 TiB minimum, EFS latency and burst-credit statements, the Longhorn RWX row, the claims that plain NFS ignores quotas, that SQLite and most databases corrupt on NFS, that `soft` mounts risk data loss and that stale file handles follow server failover, and the Filestore provisioner name.

Method: documentation only; no commands were run.
