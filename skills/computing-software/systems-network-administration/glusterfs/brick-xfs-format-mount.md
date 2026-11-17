---
id: computing-software.systems-network-administration.glusterfs.brick-xfs-format-mount
name: brick-xfs-format-mount
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, brick, xfs, mkfs, fstab]
level: practitioner
status: docs-checked
description: "Format a GlusterFS brick with XFS using 512-byte inodes, add the fstab entry with inode64 and noatime, mount it and check with df."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/formatting-and-mounting-bricks.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Quick-Start-Guide/Quickstart.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Format and mount a brick with XFS

Format the device (for example the thin LV `/dev/gfs_vg/gfs_lv`). The 512-byte inode size leaves room for GlusterFS extended attributes.

```
mkfs.xfs -f -i size=512 -n size=8192 -d su=128k,sw=10 DEVICE
```

Create the mount point and add an fstab line:

```
mkdir /mountpoint
/dev/gfs_vg/gfs_lv    /mountpoint  xfs rw,inode64,noatime,nouuid      1 2
```

Mount and check:

```
mount /mountpoint
df -h
```

`df -h` should list the device at the mount point.

For a simple test setup, the Quick Start uses `mkfs.xfs -i size=512 /dev/sdb1`, `mkdir -p /data/brick1`, an fstab entry `/dev/sdb1 /data/brick1 xfs defaults 1 2`, then `mount -a && mount`. Gluster is designed to work on any filesystem that supports extended attributes, but XFS is what the guides use.

## Checked

2026-11-04: the mkfs.xfs line, the 512-byte inode reason, mkdir, the fstab line, mount and `df -h`, and the Quick Start test setup were read against the glusterdocs pages formatting-and-mounting-bricks and Quick-Start-Guide Quickstart. Removed the advice to match `su` and `sw` to the hardware stripe, which the page does not state.

Method: documentation only; no commands were run.
