---
id: computing-software.systems-network-administration.zfs.zpool-get-set-properties
name: zpool-get-set-properties
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, get, set, properties, vdev-properties, json]
level: practitioner
status: docs-checked
description: "Read and change ZFS pool and vdev properties with zpool get and zpool set: field selection, scripted and JSON output, and the vdev form."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-get.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool get and set

## get

```
zpool get [-Hp] [-j [--json-int, --json-pool-key-guid]] [-o field[,field]...] all|property[,property]... [pool]...
zpool get [-Hp] [-j [--json-int]] [-o field[,field]...] all|property[,property]... pool [all-vdevs|vdev]...
```

Pool form: shows the named properties, or `all`, for the listed pools or all pools. Properties are in zpoolprops(7). Vdev form: shows properties for named vdevs or `all-vdevs` within a pool; see vdevprops(7).

```
zpool get all tank
zpool get capacity,health tank
zpool get -Hp -o name,value size tank
zpool get all tank all-vdevs
zpool get -j --json-int size tank
```

## Options

- `-o`: columns to show. Default `name,property,value,source`. The `source` is `default` or `local`.
- `-H`: scripted mode, no headers, tab-separated.
- `-p`: exact parsable numbers.
- `-j`: JSON. `--json-int` emits integers instead of strings. `--json-pool-key-guid` keys pool objects by GUID (pool form only).

## set

```
zpool set property=value pool
zpool set property=value pool vdev
```

The first sets a pool property, the second a vdev property. The man page lists no options for `set`.

```
zpool set comment="rack 4" tank
```

Use `source` to find what has been changed locally. For properties set at creation or import, see zpool-create-pool and zpool-import-pools.

## Checked

2026-11-03. Pages read: zpool-get(8), zpoolprops(7).

Confirmed: both get synopses, the fields name, property, value and source, -o default, -H, -p, -j with --json-int and --json-pool-key-guid, set pool and vdev forms, and the comment pool property.

Method: documentation only; no commands were run.
