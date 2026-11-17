---
id: computing-software.cloud-infrastructure-engineering.openebs.rawfile-storageclass-parameters
name: rawfile-storageclass-parameters
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, rawfile, storageclass, fstype, thinprovision, formatoptions, copyonwrite, freezefs, mountoptions]
level: practitioner
status: docs-checked
description: "Configure Local PV Rawfile StorageClass parameters: fstype, thinProvision, formatOptions, copyOnWrite, freezeFs, mountOptions, with defaults and the string-value rule."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-rawfile/configuration/rawfile-storageclass-parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The driver matches parameter keys **case-insensitively** and expects string values, so booleans must be quoted as `"true"` or `"false"`.

- **`fstype`** (optional): `ext4` (default), `xfs` or `btrfs`. If unset, the node plugin's `defaultFs` applies (chart value `node.defaultFs`). Ignored for `volumeMode: Block` PVCs.
- **`thinProvision`**: `"false"` (default) pre-allocates the whole backing file, so no overprovisioning. `"true"` uses a sparse file and allows overprovisioning; you must then watch `rawfile_pool_remaining_capacity_bytes` so the backing filesystem does not fill.
- **`formatOptions`**: extra flags for `mkfs.<fstype>`, applied only at first format. Examples from the page: ext4 `"-m 0"` removes the 5% root-reserved blocks; xfs `"-i maxpct=10"` limits inode space. In Helm values it is a list that is joined with spaces.
- **`copyOnWrite`**: leave **unset** (recommended) and the driver autodetects CoW support on each pool. `"true"` requires a reflink-capable pool (btrfs, or XFS made with `-m reflink=1`). `"false"` disables CoW, useful for databases where `nodatacow` improves write performance. With CoW, snapshots and clones are cheap; without it snapshots do a full copy.
- **`freezeFs`**: `"true"` briefly runs `fsfreeze` during a snapshot of an in-use volume for a crash-consistent image. On a non-CoW pool the filesystem stays frozen for the whole copy, which can be long on big volumes.
- **`mountOptions`** is also available.

## Checked

2026-11-04. Confirmed against the Local PV Rawfile StorageClass Parameters page: case-insensitive keys and string values, `fstype` and `node.defaultFs`, `thinProvision`, `formatOptions` and its Helm list form, `copyOnWrite`, and `freezeFs`. Nothing removed.

Method: documentation only; no commands were run.
