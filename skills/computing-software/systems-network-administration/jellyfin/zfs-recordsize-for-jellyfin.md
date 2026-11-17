---
id: computing-software.systems-network-administration.jellyfin.zfs-recordsize-for-jellyfin
name: zfs-recordsize-for-jellyfin
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, zfs, recordsize, sqlite, ssd, datasets]
level: sme
status: docs-checked
description: "Set ZFS dataset record sizes of 4K or 8K for the Jellyfin SQLite data and 1M for large media, and keep Jellyfin data on SSD."
sources: ["https://jellyfin.org/docs/general/administration/storage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ZFS record size for Jellyfin

Jellyfin's database is SQLite, and ZFS defaults to a `128 K` record size, which is sub-optimal for it.

**Recommendations from the docs**
- Dataset holding the Jellyfin SQLite database: record size `4 K` or `8 K`.
- Datasets holding media: must not use `4 K` or `8 K`, or performance suffers as the database scales. For large media files `1 M` is likely appropriate.
- Do not put Jellyfin data (everything except the media files) on ZFS-formatted mechanical drives. An SSD is strongly recommended. ZFS snapshots can consume a lot of space without a `destroy` schedule, which tempts people towards cheap disks.

Containers make this easy: bind-mount the config/data path from a small dataset with the small record size and media from another dataset with the large one.

**Existing data is not rewritten.** Changing `recordsize` on an existing dataset affects only newly written blocks, so performance does not change for data already there. Rewrite the data into the dataset to benefit.

## Checked

2026-11-03. Confirmed against the Jellyfin Storage page, ZFS section: 128 K default, 4 K or 8 K for the database dataset, not for media, 1 M for large media, existing data not rewritten, SSD recommendation. Removed: an invented example procedure and an invented verify command.

Method: documentation only; no commands were run.

For SQLite settings such as `cacheSize` see `computing-software.systems-network-administration.jellyfin.database-xml-tuning`.
