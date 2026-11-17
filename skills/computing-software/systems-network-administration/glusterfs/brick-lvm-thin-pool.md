---
id: computing-software.systems-network-administration.glusterfs.brick-lvm-thin-pool
name: brick-lvm-thin-pool
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, brick, lvm, thin-pool, pvcreate]
level: advanced
status: docs-checked
description: "Build a thinly provisioned LVM volume for a GlusterFS brick: pvcreate with data alignment, vgcreate, thin pool with chunk size, disabled zeroing, and a thin LV."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/formatting-and-mounting-bricks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Brick LVM thin pool

Example from the page for device `/dev/sdb`:

```
pvcreate --dataalignment 128K /dev/sdb
vgcreate --physicalextentsize 128K gfs_vg /dev/sdb
```

Use a device-specific alignment value, and one volume group per storage device.

Thin pool: create a metadata LV and a data LV, then convert them:

```
lvcreate -L 16776960K --name gfs_pool_meta gfs_vg
lvcreate -L 536870400K --name gfs_pool gfs_vg
lvconvert --chunksize 1280K --thinpool gfs_vg/gfs_pool --poolmetadata gfs_vg/gfs_pool_meta
```

Set `--chunksize` to the stripe width of your storage. Chunks are zeroed by default to stop data leaking between block devices; the page disables this:

```
lvchange --zero n gfs_vg/gfs_pool
```

Create one thin LV per thin pool:

```
lvcreate -V 1G -T gfs_vg/gfs_pool -n gfs_lv
```

Then format it (see brick-xfs-format-mount).

## Checked

2026-11-04: pvcreate and vgcreate examples, the one-VG-per-device advice, the metadata and data LVs, lvconvert with chunk size, the zeroing note with `lvchange --zero n`, and the thin LV were read against the glusterdocs page formatting-and-mounting-bricks. Removed the claim that thin LVM is required for snapshots, which the page does not state.

Method: documentation only; no commands were run.
