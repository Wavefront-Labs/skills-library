---
id: computing-software.cloud-infrastructure-engineering.garage.metadata-auto-snapshot-interval
name: metadata-auto-snapshot-interval
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [metadata-auto-snapshot-interval, scheduled-snapshots, garage-meta-snapshot, metadata-recovery]
level: advanced
status: docs-checked
description: "Schedule consistent live snapshots of the metadata database and know how Garage retains them."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`metadata_auto_snapshot_interval` (since v0.9.4) makes Garage copy its metadata database file at a regular interval, into the metadata directory or `metadata_snapshots_dir` if that is set. The value is any duration string accepted by the `fundu_systemd` crate, such as `"6h"` in the page's example.

Garage keeps only the two most recent snapshots and deletes older ones. A manual snapshot is available with `garage meta snapshot`.

The page calls Garage's own snapshots the best choice for recovery, because they are clean and consistent. Filesystem-level snapshots taken while writes are in flight may be corrupted.

Costs to expect: a snapshot is relatively intensive because the whole data file is copied, so the node may slow down. Under heavy write load, a running snapshot can make the database file grow considerably because pages cannot be recycled easily.

This setting matters most with LMDB, which is prone to corruption after an unclean shutdown; the page recommends configuring the interval to make recovery easy.

## Checked

2026-11-04. Read the Configuration file format page in full. Confirmed the v0.9.4 gate, the target directory, the fundu_systemd duration format and the 6h example, the two-snapshot retention, the manual command, the consistency remark and the cost warnings. Removed the recovery procedure and example snapshot name, which are not on the cited page.
Method: documentation only; no commands were run.
