---
id: computing-software.cloud-infrastructure-engineering.longhorn.trim-filesystem
name: trim-filesystem
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [trim, fstrim, unmap, snapshots, space-reclaim]
level: practitioner
status: docs-checked
description: "Reclaim Longhorn space with fstrim, trimming RWX volumes through the share manager, snapshot-chain removal setting and trim limitations."
sources:
  - https://longhorn.io/docs/1.13.0/nodes-and-volumes/volumes/trim-filesystem/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: return freed filesystem blocks to the disk.

Requirements: Longhorn v1.4.0+, a trimmable filesystem such as ext4 or xfs, and the volume attached and mounted.

Commands:
- RWO: `fstrim <mount point>` in the workload pod, or on the node where the volume was manually attached.
- RWX: the mount point is in the share manager pod.

```bash
kubectl -n longhorn-system exec -it <share-manager-pod> -- bash
mount | grep <volume name>
fstrim /export/<volume name>
```

- UI: the volume operation Trim Filesystem on attached volumes.

Snapshot removal: the global setting Remove Snapshots During Filesystem Trim, when enabled, marks the latest snapshot and the preceding continuous chain as removed. Per-volume override `volume.Spec.UnmapMarkSnapChainRemoved` takes `disabled`, `enabled` or `ignored` (defer to global); The value can also be configured in a StorageClass so it applies to all volumes created from it. The `discard` mount option frequently triggers snapshot removal and can interrupt backup creation.

Limitations:
- No effect while a rebuild is in progress.
- During expansion, trim returns an I/O error.
- Encrypted volumes: TRIM commands are not enabled by the device-mapper by default; on the attached node run `cryptsetup --allow-discards --persistent refresh <volume name>`, then trim via the UI or `fstrim` on the mount of `/dev/mapper/<volume name>`.

## Checked

2026-11-08. Confirmed against: https://longhorn.io/docs/1.13.0/nodes-and-volumes/volumes/trim-filesystem/. Version and filesystem prerequisites, UI and fstrim methods, RWO and RWX mount points with the share manager steps, the snapshot-removal global setting and per-volume field values, the discard warning, rebuild, expansion and encrypted-volume limitations.

Removed or reworded: The explicit StorageClass parameter name (the page only says it can be set in a StorageClass).

Method: documentation only; no commands were run.
