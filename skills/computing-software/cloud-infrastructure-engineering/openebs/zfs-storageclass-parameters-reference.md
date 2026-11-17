---
id: computing-software.cloud-infrastructure-engineering.openebs.zfs-storageclass-parameters-reference
name: zfs-storageclass-parameters-reference
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, zfs, storageclass, poolname, recordsize, volblocksize, compression, dedup, quotatype, thinprovision]
level: practitioner
status: docs-checked
description: "Choose Local PV ZFS StorageClass parameters: required poolname, fstype, recordsize vs volblocksize, compression, dedup, logbias, quotatype, thinProvision, dataset vs ZVOL."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-zfs/configuration/zfs-storageclass-parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Standard fields sit at the top of the class: `allowVolumeExpansion`, `mountOptions`, `volumeBindingMode` (`Immediate` or `WaitForFirstConsumer`), `reclaimPolicy` (`Delete` or `Retain`) and `allowedTopologies`. ZFS-specific settings go under `parameters`.

The only **required** parameter is `poolname`: an existing ZFS pool or child dataset, such as `zfspv-pool` or `zfspv-pool/child`.

Whether a parameter applies depends on `fstype`:

- With `fstype: zfs` the volume is a **dataset**, and dataset parameters take effect.
- With any other filesystem (`ext2`, `ext3`, `ext4`, `xfs`, `btrfs`) the volume is a **ZVOL** with a filesystem on top, and ZVOL parameters take effect.

| Parameter | Values | Applies to |
|---|---|---|
| `recordsize` | power of 2, 512 bytes to 128 KiB | dataset |
| `volblocksize` | power of 2, 512 bytes to 128 KiB | ZVOL |
| `formatOptions` | extra `mkfs` options | ZVOL |
| `compression` | on, off, lzjb, lz4, zle, gzip, gzip-1 to -9, zstd, zstd-fast, zstd-1 to -19 | both |
| `dedup` | on, off | both |
| `atime` | on, off | dataset |
| `logbias` | latency, throughput | both |
| `thinProvision` | yes, no | both |
| `quotatype` | quota, refquota | dataset |
| `shared` | yes, no | both |

`quotatype` selects the ZFS property that enforces the volume size: `quota` also counts snapshots and clones, `refquota` does not. It cannot be changed once the volume is provisioned, and the default is `quota`.

## Checked

2026-11-04. Confirmed against the Local PV ZFS StorageClass Parameters page: standard fields, required `poolname`, the dataset versus ZVOL split by `fstype`, every parameter value in the table, and the `quotatype` behaviour. Replaced the unsupported resize-time claim.

Method: documentation only; no commands were run.
