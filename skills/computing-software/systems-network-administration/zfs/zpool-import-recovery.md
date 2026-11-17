---
id: computing-software.systems-network-administration.zfs.zpool-import-recovery
name: zpool-import-recovery
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, import, recovery, rewind, txg, missing-log]
level: sme
status: docs-checked
description: "Recover an unimportable ZFS pool with zpool import -F, -n, -X, -T, -m and -M, and rewind to a checkpoint; what each discards and the risk."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-import.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Import recovery options

These options can discard data. The man page marks -X, -T and -M as last resorts and says -F is ignored when the pool is already importable.

## 1. Check with -F -n

```
zpool import -F -n tank
```

`-F` is recovery mode: it discards the last few transactions to make a non-importable pool importable. Discarded data is permanently lost. `-n` with `-F` only reports whether recovery is possible. `-F` is ignored if the pool is already importable or imported.

```
zpool import -F tank
```

## 2. Missing log device: -m

`-m` allows import when a log device is missing. Recent transactions may be lost.

## 3. Last resorts

- `-X` (with `-F`): extreme measures to find a valid txg, even one not guaranteed consistent. May leave uncorrectable checksum errors.
- `-T txg`: roll back to a specific txg; implies `-FX`, same risks.
- `-M`: import despite damaged non-critical metadata (indirect block, directory, dnode block). Affected objects become inaccessible, their space leaks, and they may be impossible to remove.

## Checkpoint rewind

```
zpool import --rewind-to-checkpoint tank
```

Rewinds to the checkpoint; this cannot be undone and later changes are lost. If the readonly option is enabled, the checkpointed state is opened without rewinding so you can see how the pool would look (the `readonly=on` pool property imports read-only):

```
zpool import -o readonly=on --rewind-to-checkpoint tank
```

## Checked

2026-11-03. Pages read: zpool-import(8), zpoolprops(7).

Confirmed: -F, -n, -m, -X, -T (implies -FX), -M and --rewind-to-checkpoint, and the readonly pool property.

Removed or corrected: the advice to copy the devices first and the claim that every option loses data (-n does not).

Method: documentation only; no commands were run.
