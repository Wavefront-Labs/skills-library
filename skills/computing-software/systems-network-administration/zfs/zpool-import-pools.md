---
id: computing-software.systems-network-administration.zfs.zpool-import-pools
name: zpool-import-pools
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, import, altroot, cachefile, rename, encryption]
level: practitioner
status: docs-checked
description: "Find and import ZFS pools with zpool import: listing, search paths, renaming, temporary names, altroot, -N, -l keys, destroyed pools and forcing."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-import.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool import

Forms:

```
zpool import [-D] [-d dir|device]...            # list
zpool import -a [-DflmMN] [-c cachefile|-d dir|device] [-o mntopts] [-o property=value]... [-R root] [-s]
zpool import [-DflmMt] [...] pool|id [newpool]
```

Listing shows each pool name, numeric ID, vdev layout and per-device health. Use the numeric ID when two pools share a name.

## Discovery

- Default search uses libblkid on Linux and geom on FreeBSD.
- `-d dir|device`: search a directory or use a file/device; repeatable; not with `-c`.
- `-c cachefile`: read config from a cachefile instead of scanning.
- `-s`: scan the default path without the libblkid cache. `ZPOOL_IMPORT_PATH` sets a custom search path.

## Examples

```
zpool import
zpool import tank
zpool import 15451357997522795478 newtank
zpool import -t tank tmpname
```

## Options

- `-a`: import every pool with enough devices.
- `-N`: do not mount filesystems.
- `-l`: request encryption keys as the pool comes online; `keylocation=prompt` datasets block until keys are entered. Without it, encrypted datasets stay unavailable until keys are loaded.
- `-o mntopts` and `-o property=value`: mount options and pool properties.
- `-R root`: sets `cachefile=none` and `altroot=root`.
- `-t`: with `newpool`, temporary name until export (original restored on export); also `cachefile=none`.
- `-f`: force a pool that looks active, e.g. devices removed without export.
- `-D`: list destroyed pools; with a pool, import one (needs `-f`).

See zpool-import-recovery for -F, -X, -T, -m and -M.

## Checked

2026-11-03. Pages read: zpool-import(8).

Confirmed: the three command forms, search behaviour, -d/-c/-s/ZPOOL_IMPORT_PATH, numeric pool ID, -a, -N, -l, -o, -R, -t, -f and -D.

Method: documentation only; no commands were run.
