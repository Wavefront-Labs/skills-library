---
id: computing-software.systems-network-administration.zfs.zfs-destroy-snapshot-ranges
name: zfs-destroy-snapshot-ranges
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, destroy, snapshot, range, deferred-destroy, retention]
level: advanced
status: docs-checked
description: "Delete ZFS snapshots by name, list or inclusive % range, defer destruction with -d, and understand eligibility via defer_destroy and userrefs."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-destroy.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Destroying snapshots

```
zfs destroy [-Rdnprv] filesystem|volume@snap[%snap[,snap[%snap]]]...
```

## Ranges and lists

- `%` joins two snapshots into an inclusive range: `tank/data@a%d`.
- Either end of a range may be blank, meaning the oldest or newest snapshot: `tank/data@%c` or `tank/data@c%`.
- Commas separate several snapshots or ranges of the same dataset: `tank/data@a,c%f`.
- With ranges or lists, give only the short name after `@`.

```
zfs destroy -nv tank/data@2026-01%2026-03
zfs destroy tank/data@2026-01%2026-03
```

Preview first with `-n` plus `-v` or `-p`.

## Flags

- `-r`: also destroy (or mark) snapshots with the same name on descendant filesystems.
- `-d`: instead of an error for an ineligible snapshot, mark it for deferred automatic destruction.
- `-R`: destroy clones of the snapshots too (and makes `-d` ineffective).

## Eligibility

A snapshot cannot be destroyed while it has clones or holds. Without `-d`, the command exits with an error and does nothing. Eligibility and marking show in the read-only properties `defer_destroy` and `userrefs`. A snapshot marked for deferred destruction stays visible; you can still clone it or add holds.

## Checked

2026-11-03. Confirmed against zfs-destroy(8): snapshot synopsis, `%` ranges with blank ends, comma lists and short names, `-r`, `-d`, `-R` (makes `-d` ineffective), `defer_destroy`, `userrefs`.
Method: documentation only; no commands were run.
