---
id: computing-software.cloud-infrastructure-engineering.openebs.hostpath-ext4-quota-prerequisites
name: hostpath-ext4-quota-prerequisites
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, hostpath, ext4, quota, prjquota, tune2fs, e2fsprogs, project-feature]
level: advanced
status: docs-checked
description: "Prepare ext4 for Local PV Hostpath quotas: install quota and e2fsprogs, enable project and quota features with tune2fs, mount with prjquota; 256-byte inodes needed."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-hostpath/advanced-operations/ext4-quota/ext4-quota-pre
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The ext4 path differs from XFS because the filesystem must have specific features turned on before project quota can work.

1. Install `quota` (provides `repquota` and `setquota`) and `e2fsprogs` (provides `tune2fs`, `chattr`, `lsattr`) on the node.
2. Check that the BasePath filesystem is ext4 with `df -Th /var/openebs/local`; if the directory does not exist yet, use the page's loop to inspect the nearest existing parent.
3. **Enable the features.** Unlike XFS, an ext4 filesystem needs `project` and `quota` features. Older `mkfs.ext4` versions may not have enabled them. List the features of the device first (the example shows neither). Then unmount, run a filesystem check (recommended before changing features), enable `project` and `quota`, and list the features again to confirm both appear. The features cannot be changed while mounted.
4. **Mount with `prjquota`.** For the root filesystem add `rootflags=prjquota` to `GRUB_CMDLINE_LINUX`, regenerate `grub.cfg`, and reboot. For a data disk, mount with the `prjquota` option and put `defaults,prjquota` in `/etc/fstab`.

The `project` feature requires an inode size of 256 bytes or more, which is the `mkfs.ext4` default. A filesystem created with a smaller inode size cannot be converted and must be recreated. After this, enable EXT4 quota as described in the Enable EXT4 Quota guide.

## Checked

2026-11-04. Confirmed against the EXT4 Quota Prerequisites page: the packages and the commands each provides, the `df -Th` check, `project` and `quota` features via `tune2fs`, the 256-byte inode note, `rootflags=prjquota` in `GRUB_CMDLINE_LINUX`, and `defaults,prjquota` in fstab. Removed the EXT4Quota StorageClass sentence, which is not on this page.

Method: documentation only; no commands were run.
