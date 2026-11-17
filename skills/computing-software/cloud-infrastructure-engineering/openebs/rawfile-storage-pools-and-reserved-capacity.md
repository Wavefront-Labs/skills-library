---
id: computing-software.cloud-infrastructure-engineering.openebs.rawfile-storage-pools-and-reserved-capacity
name: rawfile-storage-pools-and-reserved-capacity
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, rawfile, storage-pools, reserved-capacity, tiering, defaultpool, helm-values, cow]
level: advanced
status: docs-checked
description: "Define Local PV Rawfile storage pools in Helm values (node.storagePools, node.defaultPool), pick plain or subtract-from-total reserved capacity, follow the naming rules."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-rawfile/advanced-operations/rawfile-storage-pools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Storage pools give each node one or more named locations, such as an NVMe pool and an HDD pool, each on its own filesystem with its own reserved capacity. Workloads pick a tier by naming the pool in the StorageClass.

Configure pools in Helm values under `node.storagePools`. A `node.defaultPool` is required and must reference one of the defined pools. Apply with a Helm upgrade.

**Naming.** Pool names must be DNS-compatible: 3 to 63 characters, only letters, digits and hyphens, and not starting or ending with a hyphen.

**Reserved capacity modes** define how much space stays for non-pool use:

| Mode | Behaviour | Example |
|---|---|---|
| `plain` | pool grows until the given capacity remains free on the backing filesystem; for shared disks | 1 TB disk, `reservedCapacity: "10%"` allows up to 900 GB |
| `subtract-from-total` | pool capped at total size minus the reserve; for dedicated disks | 1 TB disk, `reservedCapacity: 20GiB` caps the pool at 980 GB |

**Validation at driver start.** Pool paths must exist or be creatable on each node; each pool must be on a distinct backing filesystem (no two pools on one device); `defaultPool` must name an existing pool; and paths must be unique per node.

**CoW pools.** Snapshots and clones always work, but pools on reflink-capable filesystems make them fast and space-efficient, while others do a full data copy. btrfs is native; XFS needs reflink enabled at format time.

## Checked

2026-11-04. Confirmed against the Local PV Rawfile Storage Pools page: Helm keys, naming rules, both reserved-capacity modes with their examples, the startup validation rules and the CoW notes. Nothing removed.

Method: documentation only; no commands were run.
