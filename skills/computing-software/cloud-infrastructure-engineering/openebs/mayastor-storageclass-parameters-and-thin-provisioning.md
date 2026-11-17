---
id: computing-software.cloud-infrastructure-engineering.openebs.mayastor-storageclass-parameters-and-thin-provisioning
name: mayastor-storageclass-parameters-and-thin-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [replicated-pv-mayastor, storageclass, repl, fstype, thin, formatoptions, encrypted, poolcommitment, allowvolumeexpansion]
level: practitioner
status: docs-checked
description: "Configure a Mayastor StorageClass: fsType (xfs recommended), nvmf protocol, repl, thin provisioning with commitment limits, formatOptions, overrideGlobalFormatOpts, encrypted."
sources:
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/configuration/rs-storage-class-parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All StorageClass parameters take **string values**. The `local` parameter was deprecated in version 2.0 as a breaking change and must not be used.

- **`fsType`**: `ext4` (default), `xfs` or `btrfs`. The docs recommend xfs as more advanced and performant. The filesystem driver must be installed on all worker nodes.
- **`protocol`**: `nvmf`, NVMe over TCP, used to mount the volume target on the application node.
- **`repl`**: a number above zero; the control plane keeps this many data copies where possible. 1 tolerates no node failure, 2 tolerates one, 3 tolerates two.
- **`thin`**: add `thin: true` for thin provisioning. Volumes are thick by default. All replicas of a volume are either thick or thin, never mixed.
- **`allowVolumeExpansion`** must be true to resize volumes.
- **`formatOptions`**: extra mkfs options for the chosen filesystem.
- **`overrideGlobalFormatOpts`**: a Helm key defines global xfs format options applied to all xfs volumes. Set this to `true` to override them for one volume; if both are given they are concatenated, so for edits pass the flags in `formatOptions`.
- **`encrypted`**: true enables encryption; the volume is provisioned only if available encrypted pools number at least `repl`.
- **`snapshotRestorePolicy`**: `strict` (default) or `bestEffort`; see the restore skill.

**Thin provisioning obligations.** Monitor pool usage with the exporter metrics. When a multi-replica pool runs out of space, the largest out-of-space replica is moved, so add pools or delete volumes before volumes degrade or fault. The Helm `agents.core.capacity.thin` block has `poolCommitment` (maximum pool commitment percent), `volumeCommitment` (minimum free space, as a percent of volume size, needed in each pool to add replicas to an existing volume) and `volumeCommitmentInitial` (the same for a new volume). A volume larger than a pool cannot be created on it.

## Checked

2026-11-04. Confirmed against the Replicated PV Mayastor StorageClass Parameters page: every parameter, value and default listed above, the `agents.core.capacity.thin` fields, and the thick-by-default and all-thick-or-all-thin rules. Removed the unsupported claim that `allowVolumeExpansion` defaults to true since 2.6.0.

Method: documentation only; no commands were run.
