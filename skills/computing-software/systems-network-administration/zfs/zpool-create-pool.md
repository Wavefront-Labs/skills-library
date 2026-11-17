---
id: computing-software.systems-network-administration.zfs.zpool-create-pool
name: zpool-create-pool
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, create, pool, features, compatibility, altroot]
level: practitioner
status: docs-checked
description: "Create a ZFS pool with zpool create: dry runs, pool and root-dataset properties, feature control, compatibility sets, altroot, naming rules and safety checks."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-create.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool create

```
zpool create [-dfn] [-m mountpoint] [-o property=value]... [-o feature@feature=value] [-o compatibility=off|legacy|file[,file]...] [-O file-system-property=value]... [-R root] [-t tname] pool vdev...
```

Preview with `-n`:

```
zpool create -n tank mirror sda sdb
```

`-n` prints the configuration without creating it; creation can still fail on privileges or device sharing.

## Options

- `-m mountpoint`: root dataset mountpoint (default `/pool`); an absolute path, `legacy` or `none`.
- `-o property=value`: pool properties (zpoolprops(7)). `-O` sets properties on the root file system instead.
- `-d`: enable no features; enable individual ones with `-o feature@name=enabled`.
- `-o compatibility=...`: restrict features to a compatibility set so the pool imports on other ZFS releases.
- `-R root`: shorthand for `-o cachefile=none -o altroot=root`.
- `-t tname`: temporary in-core name; sets `cachefile` default to `none`.
- `-f`: force use of devices that appear in use or have a conflicting replication level. Some cannot be overridden.

## Naming

Start with a letter; allowed characters are alphanumerics, `_`, `-`, `:`, space and `.`. The names `mirror`, `raidz`, `draid`, `spare` and `log` (and names beginning with the first four) are reserved.

## Safety

Never use one device in two pools; that corrupts them. Avoid running `replace`, `create`, `add` or `labelclear` on the same device at once. By default all supported features are enabled.

## Checked

2026-11-03. Pages read: zpool-create(8).

Confirmed: synopsis, -n, -m, -o, -O, -d, compatibility, -R, -t, -f, naming rules and reserved names, device-sharing warning, default features.

Method: documentation only; no commands were run.
