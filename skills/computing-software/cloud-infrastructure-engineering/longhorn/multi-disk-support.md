---
id: computing-software.cloud-infrastructure-engineering.longhorn.multi-disk-support
name: multi-disk-support
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [multidisk, disks, block-disk, storage-reserved, filesystem-disk]
level: practitioner
status: docs-checked
description: "Add Longhorn filesystem and block disks to a node, set storageReserved, avoid duplicate paths, and remove disks safely."
sources:
  - https://longhorn.io/docs/1.13.0/nodes-and-volumes/nodes/multidisk/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add and remove disks on a Longhorn node.

Types: `diskType: filesystem` for the V1 engine (ext4 or xfs mounted on the host); `diskType: block` for V2 (raw device). V1 volumes use only filesystem disks, V2 only block disks. The default disk is a filesystem disk at `/var/lib/longhorn`.

Add a filesystem disk: format and mount it (for example `/mnt/example-disk`), then in the UI use Nodes, node, Edit Disks, or `kubectl edit node.longhorn.io <node-name>`:

```yaml
example-disk:
  allowScheduling: true
  diskDriver: ""
  diskType: filesystem
  evictionRequested: false
  path: /mnt/example-disk
  storageReserved: 0
  tags: []
```

A path already used by another Longhorn disk is rejected, as is a disk with the same filesystem ID as another disk on the node. For an alternate path use `mount --bind`, not symlinks, and persist it (for example `/etc/fstab`).

Add a block disk: needs the V2 engine enabled. Run `wipefs -a /path/to/block/device` first; disks with a filesystem or partition table are refused. Use `diskType: block` with `diskDriver` one of `auto`, `aio`, `nvme`, `virtio-blk`. `path` is a BDF such as `0000:05:00.0` for NVMe or VirtIO, or a device path for AIO; prefer `/dev/disk/by-id/...`. Check `node.status.diskStatus`.

Reserved space: `spec.disks.<name>.storageReserved` in bytes. The default disk reserves 30% via `storage-reserved-percentage-for-default-disk`; block disks have no automatic reservation.

Remove: disable scheduling, evict all replicas and backing images (including errored ones), then delete the disk from the configuration.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/nodes-and-volumes/nodes/multidisk/

No claim needed changing.

Method: documentation only; no commands were run.
