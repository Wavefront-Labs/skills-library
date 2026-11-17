---
id: computing-software.cloud-infrastructure-engineering.garage.metadata-snapshots-dir-space
name: metadata-snapshots-dir-space
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [metadata-snapshots-dir, snapshot-disk-space, metadata-snapshot]
level: advanced
status: docs-checked
description: "Relocate metadata snapshots with metadata_snapshots_dir because they can need up to four times the database size."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
  - https://garagehq.deuxfleurs.fr/documentation/operations/upgrading/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`metadata_snapshots_dir` (since v1.1.0) is the directory where Garage writes snapshots of the metadata database. Snapshots occur when an RPC call asks for one, or regularly through `metadata_auto_snapshot_interval`.

If unset, snapshots go to a `snapshots/` subdirectory of `metadata_dir`. That can fill the metadata disk quickly. Each snapshot needs roughly as much space as the original database, and Garage temporarily holds up to three snapshots before deleting the oldest to return to two. The page therefore says to plan for up to 4x the existing metadata database.

To avoid exhausting a small SSD, point the setting at a directory with ample space, for example on the same storage as `data_dir`:

`metadata_snapshots_dir = "/path/to/snapshots"`

Related behaviour from the same page: Garage keeps only the two most recent snapshots and removes older ones automatically; a manual snapshot can be taken with `garage meta snapshot`; taking one is intensive because the whole file is copied, which can slow the node, and under heavy write load it can make the database file grow because pages cannot be recycled easily.

The upgrading page notes that since v0.9.4 `garage meta snapshot --all` takes a simultaneous snapshot of the metadata databases of all nodes, and that with automatic snapshotting Garage keeps only the last two snapshots.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Configuration file format, Upgrading Garage. Confirmed on the configuration page: `metadata_snapshots_dir` (since v1.1.0), the default `snapshots/` subdirectory, the up-to-4x space reasoning, two snapshots kept, intensive copy, and database growth under write load. Confirmed on the upgrading page: `garage meta snapshot --all` (since v0.9.4). Removed: the inference that this directory must have room for upgrade snapshots.

Method: documentation only; no commands were run.
