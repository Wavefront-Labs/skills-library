---
id: computing-software.systems-network-administration.zfs.zfs-promote-clone
name: zfs-promote-clone
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, promote, clone, origin, snapshot-ownership]
level: practitioner
status: docs-checked
description: "Promote a ZFS clone with zfs promote so the origin dataset can be destroyed, and resolve snapshot name conflicts and space accounting."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-promote.8.html
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-rename.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Promoting a clone

```
zfs promote clone
```

Promotion reverses the parent-child relationship between a clone and the dataset it came from, so you can destroy the original (its origin) afterwards.

## What moves

The snapshot the clone was created from, and any older snapshots, transfer to the promoted clone. Their space accounting moves too, so enough space must be available to accommodate them. Promotion itself consumes no new space; only the accounting changes.

## Name conflicts

The promoted clone must not already have snapshots whose names conflict with the ones being transferred. Rename the clone's snapshots with `zfs rename` first.

## Typical sequence

```
zfs snapshot pool/project/production@today
zfs clone pool/project/production@today pool/project/beta
# test changes in beta
zfs promote pool/project/beta
zfs rename pool/project/production pool/project/legacy
zfs rename pool/project/beta pool/project/production
zfs destroy pool/project/legacy
```

## Checked

2026-11-03. Confirmed against zfs-promote(8): reversed dependency, snapshot ownership and space accounting, no new space consumed, conflicting snapshot names, and the example sequence. Replaced the quota wording with the page's wording and removed the generic list advice.
Method: documentation only; no commands were run.
