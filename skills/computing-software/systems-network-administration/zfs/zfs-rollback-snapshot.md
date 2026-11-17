---
id: computing-software.systems-network-administration.zfs.zfs-rollback-snapshot
name: zfs-rollback-snapshot
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, rollback, snapshot, recovery, destructive]
level: practitioner
status: docs-checked
description: "Roll a ZFS dataset back to a snapshot with zfs rollback, understand -r and -R destruction of newer snapshots and clones, and per-child limits."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-rollback.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rolling back

```
zfs rollback [-Rfr] snapshot
```

Rollback discards all changes since the snapshot and returns the dataset to its state then.

```
zfs rollback -r pool/users/anne@yesterday
```

## Rules

- By default, rollback fails unless the target is the most recent snapshot.
- `-r` destroys snapshots and bookmarks newer than the target so you can reach an older one.
- `-R` destroys newer snapshots and bookmarks plus any clones of those snapshots.
- `-f` (only with `-R`) forcibly unmounts clone filesystems that are about to be destroyed.

## Recursive snapshots

`-r` and `-R` do not recursively destroy the child snapshots of a recursive snapshot. They only affect snapshots of the named filesystem. To roll back a whole tree taken with `zfs snapshot -r`, roll back each child dataset to its snapshot individually.

## Safer options

- Read-only recovery: copy files from `.zfs/snapshot/<name>` instead.
- Branch off: `zfs clone` the snapshot, inspect, then promote or discard.
- Before an `-r` rollback, list what will be destroyed with `zfs list -t snapshot -r dataset`.

## Checked

2026-11-03. Confirmed against zfs-rollback(8) (synopsis, discarded changes, most-recent-snapshot default, `-r`, `-R`, `-f`, recursive-snapshot caveat), zfs-snapshot(8) (`.zfs/snapshot` mounts) and zfs-clone(8). Removed the unsupported claim that a bookmark protects data before rollback.
Method: documentation only; no commands were run.
