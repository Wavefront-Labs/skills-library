---
id: computing-software.cloud-infrastructure-engineering.longhorn.architecture-and-components
name: architecture-and-components
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [architecture, instance-manager, engine, replicas, data-engine]
level: intro
status: docs-checked
description: "Longhorn 1.13 architecture: manager, engine, replicas, instance manager, V1 versus V2 data engines, snapshot and backup block limits."
sources:
  - https://longhorn.io/docs/1.13.0/concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know what runs where and the hard limits.

Components:
- Longhorn Manager: DaemonSet on every node; the control plane handling UI and CSI API calls.
- Longhorn Engine: one storage controller per volume, on the same node as the consuming pod.
- Replicas: hold a snapshot chain per volume, one per node or disk, built from sparse files.
- Instance Manager: one pod per node per data engine version in `longhorn-system`, named `instance-manager-<hash>`, labelled `longhorn.io/node=<node-name>`. It hosts engine and replica instances for many volumes; there is no per-volume engine pod. Debug here first.
- CSI driver: create, delete, attach, detach, mount, snapshot; other features go through the UI.

Data engines: V1 uses an iSCSI frontend and needs `open-iscsi` or `iscsiadm`. V2 runs `spdk_tgt` in the instance manager, turns each block disk into a Logical Volume Store, and uses NVMe-TCP or UBLK frontends; it reserves dedicated CPU cores and needs `vfio_pci`, `uio_pci_generic`, `nvme_tcp` (or `ublk_drv` plus hugepages).

Limits:
- N replicas tolerate N-1 failures.
- Up to 254 snapshots per volume; a 1 TB volume uses about 256 MB of read index per replica.
- The latest snapshot cannot be deleted directly.
- Backups use compressed 2 MB blocks; a changed 4K block backs up the whole block.
- Volumes are thin provisioned and do not shrink automatically.

Rebuild: a blank replica is added write-only, synced, set read-write, then the faulty replica is removed. Longhorn runs `sync` before snapshots.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/concepts/

No claim needed changing.

Method: documentation only; no commands were run.
