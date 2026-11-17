---
id: computing-software.systems-network-administration.zfs.zpool-checkpoint
name: zpool-checkpoint
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, checkpoint, rewind, discard, rollback, upgrade]
level: advanced
status: docs-checked
description: "Save and rewind ZFS pool state with zpool checkpoint: create, discard with -d and -w, import --rewind-to-checkpoint, blocked subcommands and space use."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-checkpoint.8.html
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-import.8.html
  - https://openzfs.github.io/openzfs-docs/man/master/7/zpoolconcepts.7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool checkpoint

```
zpool checkpoint [-d [-w]] pool
```

With no options, saves the current pool state so it can later be restored with `zpool import --rewind-to-checkpoint`. Take one before a risky pool-level change.

```
zpool checkpoint tank
zpool checkpoint -d tank
zpool checkpoint -d -w tank
```

- `-d` (`--discard`): remove the existing checkpoint.
- `-w` (`--wait`): with `-d`, do not return until the discard finishes.

## Rewind

Export the pool, then:

```
zpool import --rewind-to-checkpoint tank
```

This cannot be undone and later changes are lost. With the `readonly` mount option the checkpointed state opens read-only so it can be inspected first.

## Restrictions while one exists

- These subcommands are blocked: `remove`, `attach`, `detach`, `split` and `reguid`.
- If the pool lacks free space, the checkpoint may break reservation boundaries.

## Monitoring

`zpool status` shows whether a checkpoint exists and discard progress. `zpool list` shows the space it consumes (the `checkpoint` column). `zpool wait -t discard` waits for a discard.

Discard it once the change is verified, to free the space and unblock the subcommands above.

## Checked

2026-11-03. Pages read: zpool-checkpoint(8), zpool-import(8), zpoolconcepts(7), zpool-wait(8), zpool-list(8).

Confirmed: synopsis, -d and -w, rewind after export and import, irreversibility, blocked subcommands (remove, attach, detach, split, reguid), reservation caveat, status and list reporting, wait -t discard.

Method: documentation only; no commands were run.
