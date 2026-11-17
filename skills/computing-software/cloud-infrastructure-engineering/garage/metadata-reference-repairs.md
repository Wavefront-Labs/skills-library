---
id: computing-software.cloud-infrastructure-engineering.garage.metadata-reference-repairs
name: metadata-reference-repairs
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [garage-repair-tables, garage-repair-versions, block-refs, block-rc]
level: advanced
status: docs-checked
description: "Resync metadata tables and purge orphan versions, block references and reference counters."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/durability-repairs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Garage resyncs all metadata table entries automatically every hour, using a Merkle tree to find differences between nodes efficiently. Run it manually, for example before an upgrade, with `garage repair tables`.

When nodes were unavailable, references between objects can break; for instance a deleted object may leave behind its versions or data blocks. Three repairs address this:

- `garage repair versions` checks that every version belongs to a non-deleted object and purges orphan versions.
- `garage repair block-refs` checks that every block reference belongs to a non-deleted object version and purges orphan references, after which the blocks can be garbage-collected.
- `garage repair block-rc` checks that block reference counters match the real number of non-deleted entries in the block reference table.

Metadata snapshotting is the safety net for corruption. It can be done at filesystem level on ZFS or BTRFS, or by Garage itself since v0.9.4 using `metadata_auto_snapshot_interval` or the manual `garage meta snapshot`. The manual route is very intensive because it copies the full database file, so the page says you might prefer filesystem-level snapshots if possible.

Repairs need `--yes`, and `-a` runs them on all nodes: `garage repair -a --yes <name>`.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Durability & Repairs. Confirmed: hourly table resync with a Merkle tree, `garage repair tables`, the three reference repairs (versions, block-refs, block-rc), snapshot options (ZFS/BTRFS, Garage snapshots since v0.9.4, `metadata_auto_snapshot_interval`, `garage meta snapshot`), and the `--yes` and `-a` flags. Changed: softened 'the page prefers' to the page's actual wording.

Method: documentation only; no commands were run.
