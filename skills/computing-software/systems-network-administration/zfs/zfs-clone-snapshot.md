---
id: computing-software.systems-network-administration.zfs.zfs-clone-snapshot
name: zfs-clone-snapshot
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, clone, snapshot, writable-copy, test-and-replace]
level: practitioner
status: docs-checked
description: "Create a writable ZFS clone from a snapshot, set properties and parents with -o and -p, and use the clone-test-promote-replace workflow."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-clone.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloning snapshots

```
zfs clone [-pu] [-o property=value]... snapshot filesystem|volume
```

Example:

```
zfs clone pool/users/bob@yesterday pool/clone
```

A clone is writable and starts with the contents of the snapshot. It has the same type as the original (filesystem or volume) and can be placed anywhere in the hierarchy.

## Options

- `-o property=value`: set a property on the new dataset (see `zfs create`).
- `-p`: create missing parents; they mount per the inherited mountpoint. Passing `-p` twice creates them with `canmount=off`. An existing target is not an error.
- `-u`: do not mount the new filesystem.

## Test and replace workflow

1. Snapshot production (`pool/project/production@today`).
2. `zfs clone pool/project/production@today pool/project/beta`; test changes in `beta`.
3. `zfs promote pool/project/beta`.
4. Rename `production` to `legacy`, then `beta` to `production`.
5. Destroy `legacy` when no longer needed.

The origin snapshot cannot be destroyed while the clone exists; promote reverses the dependency.

## Checked

2026-11-03. Confirmed against zfs-clone(8) (synopsis, `-o`, `-p`, `-u`, example and test-and-replace sequence), zfs-destroy(8) (snapshots with clones cannot be destroyed) and zfs-promote(8).
Method: documentation only; no commands were run.
