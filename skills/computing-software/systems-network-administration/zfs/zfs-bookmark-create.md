---
id: computing-software.systems-network-administration.zfs.zfs-bookmark-create
name: zfs-bookmark-create
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, bookmark, incremental-send, replication, snapshot]
level: practitioner
status: docs-checked
description: "Create ZFS bookmarks with zfs bookmark to use as an incremental send source, including short forms and -r."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-bookmark.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bookmarks

A bookmark records the point in time a snapshot was created. It can stand in for a snapshot as the incremental source of `zfs send`.

```
zfs bookmark [-r] snapshot|bookmark newbookmark
```

Example, using the short forms:

```
zfs bookmark rpool@snapshot rpool#bookmark
zfs bookmark tank/data@snapshot #bookmark
```

`@name` is a snapshot and `#name` a bookmark; the omitted dataset is taken from the other argument, so at most one of the two may be in short form.

## Option

`-r` creates bookmarks for the named snapshot on all descendant datasets. The source must be a snapshot, not a bookmark. Descendants without that snapshot are skipped. If you give `newbookmark`, its dataset must match the source snapshot's.

## Typical flow

1. Send `tank/data@a` to the replica.
2. Bookmark it: `zfs bookmark tank/data@a tank/data#a`.
3. Later: `zfs send -i tank/data#a tank/data@b | ...`.

## Notes

- The `bookmarks` feature must be enabled on the pool.
- Bookmarking a redaction bookmark produces a regular bookmark.
- Remove one with `zfs destroy tank/data#a`.

## Checked

2026-11-03. Confirmed against zfs-bookmark(8) and zfs-destroy(8): synopsis, `-r`, short forms, redaction-bookmark note, feature requirement, bookmark destroy, and use as `zfs send -i` source. Fixed the example that put both arguments in short form (the man page takes the dataset from the other argument). Removed the unsupported space-usage claim and the snapshot-destroy step.
Method: documentation only; no commands were run.
