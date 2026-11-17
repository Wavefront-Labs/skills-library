---
id: computing-software.systems-network-administration.zfs.zfs-set-inherit
name: zfs-set-inherit
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, set, inherit, properties, user-properties, received-values]
level: intro
status: docs-checked
description: "Set ZFS properties with zfs set, use size suffixes and user properties, and revert to inherited or received values with zfs inherit -r and -S."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-set.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zfs set and zfs inherit

```
zfs set [-u] property=value [property=value]... dataset...
zfs inherit [-rS] property dataset...
```

Several `property=value` pairs can be set at once, on filesystems, volumes or snapshots. Only some properties are editable; zfsprops(7) lists them.

```
zfs set quota=500G tank/users/bob
zfs set com.example:department=12345 tank/users/bob
zfs set sharenfs='rw=@192.0.2.0/24' tank/data
```

## Values

- Numeric values may be exact or use suffixes B, K, M, G, T, P, E, Z.
- User properties use a colon-separated name such as `com.example:department`, and can be set on snapshots.
- Quote values with special characters. For `sharenfs` host rules, use fully qualified hostnames if DNS resolves names.

## -u

`zfs set -u` updates `mountpoint`, `sharenfs` and `sharesmb` without mounting or sharing the dataset.

## Inherit

`zfs inherit property dataset` clears a local setting so the value comes from an ancestor; if none sets it, the property returns to its default.

- `-r`: apply to all children.
- `-S`: revert to the received value if one exists; otherwise non-inheritable properties revert to default.

Use `zfs get -s local all dataset` to find local overrides before cleaning them up.

## Checked

2026-11-03. Confirmed against zfs-set(8) (set, get and inherit synopsis, size suffixes, user properties on snapshots, `-u`, `inherit -r`/`-S`, fully-qualified hostnames for `sharenfs` when using DNS) and the `-s local` example.
Method: documentation only; no commands were run.
