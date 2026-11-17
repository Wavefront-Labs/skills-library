---
id: computing-software.systems-network-administration.zfs.zfs-get-properties
name: zfs-get-properties
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, get, properties, source, inherited, json]
level: intro
status: docs-checked
description: "Read ZFS dataset properties with zfs get, filter by source and type, choose columns, and produce scripting-friendly or JSON output."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-get.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zfs get

```
zfs get [-r|-d depth] [-Hp] [-j [--json-int]] [-o field[,field]...] [-s source[,source]...] [-t type[,type]...] all|property[,property]... [dataset]...
```

With no dataset it covers all datasets on the system. `all` shows every property that applies to the dataset type.

```
zfs get compression,recordsize tank/data
zfs get -s local all tank/data
zfs get -r -Hp -o name,value used tank
```

## Flags

- `-r` recursive; `-d depth` limited depth.
- `-H`: no headers, tab-separated. `-p`: exact numbers.
- `-j` / `--json`, with `--json-int` for integers.
- `-o`: columns `name`, `property`, `value`, `received`, `source`, or `all`. Default is name, property, value, source; `received` is hidden by default.
- `-s`: show only sources `local`, `default`, `inherited`, `temporary`, `received` or `none`.
- `-t`: filter types (`filesystem`, `snapshot`, `volume`, `bookmark`, `all`).

## Reading the source column

`local` means set on this dataset, `inherited` from an ancestor, `default` the built-in value, `received` set by a replication stream, and `-` means none.

`zfs get -s local all dataset` shows only the properties set locally.

## Checked

2026-11-03. Confirmed against zfs-get(8): synopsis, default and available `-o` fields, `received` hidden by default, `-s` sources, `-t` types, `-j`/`--json-int`, source column values, and the `-H -o value` and `-s local` examples.
Method: documentation only; no commands were run.
