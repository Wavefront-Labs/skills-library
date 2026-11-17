---
id: computing-software.systems-network-administration.samba.vfs-shadow-copy2
name: vfs-shadow-copy2
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, vfs-shadow-copy2, shadow-copy, previous-versions, snapshots, vfs]
level: advanced
status: docs-checked
description: "Expose filesystem snapshots as Windows Previous Versions with vfs_shadow_copy2: snapdir, format, basedir, sort, localtime, snapsharepath and the naming rule."
sources:
  - https://www.samba.org/samba/docs/current/man-html/vfs_shadow_copy2.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vfs shadow copy2
Enable per share with `vfs objects = shadow_copy2`. Each snapshot must be a subdirectory of the snapshot directory named by the time. Default format `@GMT-%Y.%m.%d-%H.%M.%S`; generate one with `TZ=GMT date +@GMT-%Y.%m.%d-%H.%M.%S`.

Options and defaults:
- `shadow:snapdir` `.snapshots` (absolute used as is; relative resolves from the mount point)
- `shadow:basedir` mount point of the share root (incompatible with `snapdirseverywhere` and `crossmountpoints`)
- `shadow:format` `@GMT-%Y.%m.%d-%H.%M.%S`
- `shadow:sort` `desc` (default); `asc` for ascending; any other value (the page uses `none`) turns sorting off
- `shadow:localtime` `yes` means local-time names; `no` means UTC/GMT (the page shows `no`)
- `shadow:mountpoint` usually auto-detected
- `shadow:snapsharepath` share root inside each snapshot; no default; `shadow:snapdirseverywhere` and `shadow:basedir` are incompatible with it and disable it
- `shadow:snapdirseverywhere` `no`; needs a relative snapdir
- `shadow:crossmountpoints` `no`; used with snapdirseverywhere
- `shadow:fixinodes` `no`; hashes inode numbers for filesystems like GPFS so Restore does not fail
- `shadow:sscanf` `no` (names are a time_t value); `shadow:snapprefix` (BRE) with `shadow:delimiter` `_GMT`

The page's example for `[homes]`:
```
shadow:snapdir = /data/snapshots
shadow:basedir = /data/home
shadow:sort = desc
```
The page has no ZFS, LVM or btrfs recipes. For btrfs see vfs-zfsacl-btrfs. The page stresses this is an end-user tool, not a backup, archival or version-control solution.

## Checked
2026-11-04: format, option defaults, incompatibilities and the example compared with the vfs_shadow_copy2 man page. Fixed the sort and snapsharepath wording; removed a Windows verification line the page does not state.
Method: documentation only; no commands were run.
