---
id: computing-software.systems-network-administration.zfs.zfs-destroy-datasets
name: zfs-destroy-datasets
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, destroy, dataset, dry-run, recursive, dependents]
level: practitioner
status: docs-checked
description: "Destroy ZFS datasets and bookmarks safely with zfs destroy, using -n -v dry runs and understanding -r, -R and -f."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-destroy.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Destroying datasets

```
zfs destroy [-Rfnprv] filesystem|volume
zfs destroy filesystem|volume#bookmark
```

By default the command unshares and unmounts the dataset and refuses to destroy one with dependents (children or clones).

## Always preview

```
zfs destroy -rnv tank/old
```

`-n` is a dry run, and `-v` or `-p` (parsable) report what would be deleted.

## Flags

- `-r`: recursively destroy children.
- `-R`: recursively destroy all dependents, including clones outside the target hierarchy.
- `-f`: forcibly unmount filesystems. No effect on volumes or unmounted filesystems.
- `-v` / `-p`: verbose / machine-parsable output about deleted data.

The man page warns to use `-r` and `-R` with extreme care: they can destroy large parts of a pool and cause unexpected behaviour for mounted filesystems that are in use.

## Bookmarks

`zfs destroy dataset#bookmark` removes only that bookmark.

## Before you run it

- Check dependents: children and clones block a plain destroy.
- Check holds on snapshots: a held snapshot blocks destruction (see zfs-hold-release).

## Checked

2026-11-03. Confirmed against zfs-destroy(8): synopsis, default unshare/unmount and dependents refusal, `-R`, `-f`, `-n`, `-p`, `-r`, `-v`, the warning about `-r`/`-R`, bookmark destroy, and the held-snapshot EBUSY behaviour (zfs-hold(8)). Removed the unsupported `origin` listing and the generic backup bullet.
Method: documentation only; no commands were run.
