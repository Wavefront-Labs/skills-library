---
id: computing-software.cloud-infrastructure-engineering.longhorn.rwx-volumes
name: rwx-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [rwx, nfs, share-manager, nfs-options, migratable]
level: advanced
status: docs-checked
description: "Longhorn ReadWriteMany volumes: NFSv4 client requirement, nfsOptions defaults, share manager placement, 90 second grace period and migratable volumes."
sources:
  - https://longhorn.io/docs/1.13.0/nodes-and-volumes/volumes/rwx-volumes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: provision and operate RWX volumes.

Requirements: an NFSv4 client on every node (otherwise mounts fail with a missing `/sbin/mount.<type>` helper) and unique node hostnames.

Create: access mode `ReadWriteMany` with `parameters.migratable: "false"`; a PVC's access mode applies to dynamically provisioned volumes.

Placement parameters: `shareManagerNodeSelector` (`key:value` pairs separated by `;`, merged with the global `system-managed-components-node-selector`), `allowedTopologies`, `shareManagerTolerations` (merged with global `taint-toleration`).

Mount options via `nfsOptions`: defaults are NFSv4.1, `softerr`, `timeo=600`, `retrans=5` (falls back to `soft` if `softerr` is unsupported). Supply the full set; omitted options fall back to NFS server defaults. Example `"vers=4.2,noresvport,softerr,timeo=600,retrans=5"`. Longhorn does not validate it; invalid options mean the volume is neither created nor attached. v1.4.0-1.4.3 and v1.5.0-1.5.1 hard-mount by default; use v1.4.4, v1.5.2 or later.

Failure handling:
- If the share-manager pod is terminated, client I/O blocks until a new one is created, then a 90-second grace period starts; READ/WRITE and non-reclaim locks fail with `NFS4ERR_GRACE`. Unreclaimed locks are discarded and clients see I/O errors.
- Fast failover shortens the grace period from 90 to 30 seconds.
- A Kubernetes DNS outage stops creating, deleting and recovering RWX volumes; keep DNS highly available.

Migratable RWX (KubeVirt): `volumeMode: Block`, ReadWriteMany, StorageClass `migratable: "true"`; `Filesystem` mode is not supported.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/nodes-and-volumes/volumes/rwx-volumes/

No claim needed changing.

Method: documentation only; no commands were run.
