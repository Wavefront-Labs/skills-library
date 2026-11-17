---
id: computing-software.cloud-infrastructure-engineering.garage.recover-corrupted-metadata-db
name: recover-corrupted-metadata-db
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [corrupted-metadata, snapshot-restore, db-lmdb, repair-tables]
level: advanced
status: docs-checked
description: "Repair a corrupted metadata database by resyncing from peers or restoring a Garage or filesystem snapshot."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/recovering/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A power cut can corrupt the metadata database. You can recover without changing node ID or rebuilding the layout, so no blocks move; the aim is to replace the broken file. First find it in the metadata directory according to `db_engine`.

Option 1, resync from peers (needs 2 or 3 copies): stop Garage, delete the database file or directory, restart, then run `garage repair -a --yes tables`. This takes a while as the node receives tables over the network.

Option 2, restore a Garage snapshot (since v0.9.4). Files sit in `<metadata_dir>/snapshots`, named by UTC time (the configuration page says snapshots go to `metadata_snapshots_dir` instead when that is set). Stop Garage, then for LMDB:

`mv db.lmdb db.lmdb.bak`
`cp -r snapshots/2024-03-15T12:13:52Z db.lmdb`

For Sqlite, move `db.sqlite` aside and copy the snapshot file to `db.sqlite`. Restart and run `garage repair -a --yes tables`; this is quick because only changes since the snapshot are synced. An unreplicated cluster loses changes made after the snapshot.

Option 3, roll back a ZFS or BTRFS snapshot, noting that one taken mid-write may itself be corrupt.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Configuration file format, Recovering from failures. Confirmed on the recovering page: the three options, the LMDB and Sqlite commands, snapshot location and naming, the v0.9.4 start, and the repair command. Added from the configuration page: the `metadata_snapshots_dir` override.

Method: documentation only; no commands were run.
