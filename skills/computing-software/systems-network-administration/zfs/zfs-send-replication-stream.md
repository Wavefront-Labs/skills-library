---
id: computing-software.systems-network-administration.zfs.zfs-send-replication-stream
name: zfs-send-replication-stream
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, send, replicate, replication-stream, exclude, properties]
level: advanced
status: docs-checked
description: "Replicate a ZFS dataset tree with zfs send -R, exclude datasets with -X, skip missing snapshots with -s, and send properties and holds."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-send.8.html
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-receive.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replication streams

```
zfs send [-R [-X dataset[,dataset]...]] [[-I|-i] snapshot] snapshot
```

`-R` creates a replication stream of the filesystem, all descendants, and snapshots up to the named one. It preserves properties, snapshots, descendants and clones. With `-i` or `-I`, it is an incremental replication stream.

```
zfs send -R tank/data@2026-11-03 | ssh backup zfs receive -Fu pool/backup
zfs send -R -I @2026-11-02 tank/data@2026-11-03 | ssh backup zfs receive -Fu pool/backup
```

## Options

- `-X a,b`: exclude datasets and their descendants (only with `-R`; the root cannot be excluded). `-X a -X b` equals `-X a,b`.
- `-s`: on a missing snapshot, warn and skip that dataset and its descendants instead of aborting.
- `-p`: include properties (implicit with `-R`).
- `-h`: include holds.
- `-b`: send received property values even if locally overridden.

## Receiving

On the target use `zfs receive -F` so that, for incremental replication, snapshots and filesystems that no longer exist on the sender are destroyed there. That makes the target a mirror; do not use `-F` on a target with data you want to keep.

Encrypted datasets require `-w` or `-U` with `-R`.

## Checked

2026-11-03. Confirmed against zfs-send(8) (`-R`, `-X`, `-s` only with `-R`, `-p`, `-h`, `-b`, encryption requirement) and zfs-receive(8) (`-F` destroys snapshots and filesystems missing on the sender for incremental replication streams).
Method: documentation only; no commands were run.
