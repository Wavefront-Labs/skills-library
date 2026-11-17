---
id: computing-software.systems-network-administration.samba.vfs-zfsacl-btrfs
name: vfs-zfsacl-btrfs
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, vfs-zfsacl-btrfs, zfsacl, btrfs, vfs, nfs4-acl]
level: advanced
status: docs-checked
description: "Use vfs_zfsacl for NFSv4 ACL filesystems and vfs_btrfs for clone-range copies, compression and snapshots: options, defaults and examples."
sources:
  - https://www.samba.org/samba/docs/current/man-html/vfs_zfsacl.8.html
  - https://www.samba.org/samba/docs/current/man-html/vfs_btrfs.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vfs zfsacl and btrfs
zfsacl options (defaults first):
- `nfs4:mode`: `simple` (maps only non-inheriting owner/group ACEs); `special` is deprecated.
- `nfs4:acedup`: `merge` (combine duplicate ACEs); also `dontcare`, `reject` and `ignore` (deprecated).
- `nfs4:chown`: `no`; yes enables filesystem chown and can leave the system insecure.
- `zfsacl:denymissingspecial`: `no`; yes blocks ACLs lacking owner@, group@, everyone@.
- `zfsacl:block_special`: `yes`; stops ZFS adding special entries to inherited ACLs.
- `zfsacl:map_dacl_protected`: `no`.
```
[samba_zfs_share]
    vfs objects = zfsacl
    path = /test/zfs_mount
    nfs4: mode = simple
    nfs4: acedup = merge
```
btrfs: the share path must be a Btrfs subvolume. It maps server-side copy (FSCTL_SRV_COPYCHUNK) to a clone-range ioctl, exposes per-file compression, and can drive snapshots for FSRVP.
- `btrfs: manipulate snapshots`: default `no`; yes is experimental (the page recommends `vfs_snapper` instead).
```
[share]
    vfs objects = btrfs
    btrfs: manipulate snapshots = no
```
To expose snapshots created by vfs_btrfs as previous versions, the page uses vfs_shadow_copy with `registry shares = yes` and `include = registry` in `[global]`, and `vfs objects = btrfs shadow_copy` plus `btrfs: manipulate snapshots = yes` in the share; Samba's FSRVP server must be running.

## Checked
2026-11-04: zfsacl and btrfs options, defaults and examples compared with the vfs_zfsacl and vfs_btrfs man pages. Removed: an fstype line that neither page states.
Method: documentation only; no commands were run.
