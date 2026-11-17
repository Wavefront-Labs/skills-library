---
id: computing-software.cloud-infrastructure-engineering.openebs.local-pv-engine-feature-comparison
name: local-pv-engine-feature-comparison
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, hostpath, lvm, zfs, snapshots, clones, comparison, local-storage]
level: practitioner
status: docs-checked
description: "Compare Local PV Hostpath, LVM and ZFS on snapshots, incremental backups, clones, thin provisioning and the cases where local storage is the right fit."
sources:
  - https://openebs.io/docs/concepts/data-engines/localstorage
  - https://openebs.io/docs/concepts/data-engines
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Local Storage engines create persistent volumes from local disks, hostpaths or the volume managers on worker nodes. The volume is reachable only from the node where it was created, and if that node fails the application pod is not rescheduled elsewhere.

The comparison table, from the data engines overview page:

| Feature | Hostpath | LVM | ZFS |
|---|---|---|---|
| Near-disk performance | Yes | Yes | No |
| Velero full backup/restore | Yes | Yes | Yes |
| Thin provisioning | Yes | Yes | Yes |
| On-demand expansion | Yes | Yes | Yes |
| Pool or aggregate support | Yes | Yes | Yes |
| RAID resiliency | Yes | Yes | Yes |
| Snapshots | No | Yes | Yes |
| Incremental backups | No | Yes | Yes |
| Clones | No | No | Yes |

Choose Local Storage when:

- the application manages replication and availability itself, which is typical for workloads deployed as a StatefulSet;
- dedicated local disks are unavailable or not needed for a given application;
- you need near-disk performance together with snapshots, expansion and pooling across devices.

The docs also call it well suited to short-lived stateful work such as machine learning jobs and to single-node edge clusters. The table lists only these three engines. In short, LVM gives snapshots with near-disk performance, and ZFS adds clones.

The Local Storage page lists when to avoid it: when applications expect replication from storage, or when the volume size must change dynamically and the underlying disk is not resizable. Its limitations section says Local Storage cannot sustain node failure and Hostpath does not support snapshots and clones. It also states that size cannot be increased dynamically, which sits oddly beside the table's "on-demand expansion: Yes" row; check the engine's own resize guide before relying on either.

## Checked

Method: 2026-11-08 read the raw markdown of the data engines overview page and the Local Storage page in full. The comparison table is on the overview page, not the Local Storage page the draft cited, so that source was added; the avoid-when and limitations text from the Local Storage page was added and the draft's Rawfile aside was dropped.
