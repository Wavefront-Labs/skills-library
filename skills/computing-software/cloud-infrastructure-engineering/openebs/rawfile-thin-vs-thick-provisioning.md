---
id: computing-software.cloud-infrastructure-engineering.openebs.rawfile-thin-vs-thick-provisioning
name: rawfile-thin-vs-thick-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, rawfile, thin-provisioning, thick, overprovisioning, sparse-files, monitoring]
level: practitioner
status: docs-checked
description: "Decide between thick and thin Local PV Rawfile volumes, understand overprovisioning risk, and monitor physical versus logical usage with the rawfile pool metrics."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-rawfile/advanced-operations/rawfile-thin-provisioning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rawfile volumes are **thick by default**: the backing file is fully allocated at creation. Setting `thinProvision: "true"` in the StorageClass parameters creates sparse files so only written blocks use disk, and every PVC from that class is thin.

| | Thick (default) | Thin |
|---|---|---|
| Backing file | pre-allocated | sparse |
| Disk use at creation | the requested size | near zero |
| Overprovisioning | not possible | possible |
| Performance | predictable | small latency on first write to a block |
| Risk | none, space reserved | out of space if the disk fills first |

Overprovisioning example from the page: on a 100 GB pool you could provision ten 20 GB volumes (200 GB logical) as long as total data written stays within physical capacity. If the pool runs out of physical space, writes fail with I/O errors in the application. Set alerts on `rawfile_pool_remaining_capacity_bytes` before that happens, and track the overcommit ratio using the pool's physical and logical byte metrics.

Thin works well with CoW pools: new volumes start nearly empty and snapshots or clones consume only differing blocks.

Choose thick when you need predictable I/O performance, a guaranteed reservation for a workload, or the pool is shared with other services and you want to avoid surprise out-of-space conditions.

Queries from the page: overcommit ratio is `rawfile_pool_volumes_logical_bytes / rawfile_pool_capacity_bytes`; savings ratio is `1 - (rawfile_pool_volumes_physical_bytes / rawfile_pool_volumes_logical_bytes)`; per-volume physical usage is `rawfile_volume_physical_bytes`.

## Checked

Method: 2026-11-08, read the source page (openebs/website docs markdown for rawfile-thin-provisioning) in full. Existing claims match the page; added its metric queries.
