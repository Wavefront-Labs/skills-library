---
id: computing-software.cloud-infrastructure-engineering.garage.metadata-and-data-directories
name: metadata-and-data-directories
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [metadata-dir, data-dir, ssd-metadata, node-capacity]
level: practitioner
status: docs-checked
description: "Place metadata_dir on fast storage and data_dir on bulk disks, and size node capacity from data_dir."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two directories are set in `garage.toml`.

`metadata_dir` holds the node identifier, the network configuration and peer list, the list of buckets and keys, and the index of all objects, object versions and object blocks. The page recommends a fast SSD to maximise performance.

`data_dir` holds the data blocks of objects and can live on an HDD. The space available there is what you count when setting a node's capacity in the cluster layout.

Since v0.9.0 `data_dir` can also be a list of locations, each with a `path` and either a `capacity` or `read_only = true`:

`data_dir = [ { path = "/path/to/old_data", read_only = true }, { path = "/path/to/new_hdd1", capacity = "2T" } ]`

The multi-HDD page covers operating that setup.

The default location of snapshots is a `snapshots/` subdirectory of `metadata_dir`, and the LMDB, Sqlite and Fjall databases live inside it as `db.lmdb/`, `db.sqlite` and `db.fjall/`.

## Checked

2026-11-04. Read the Configuration file format page in full. Confirmed what each directory holds, the SSD and HDD advice, the capacity note, the v0.9.0 multi-directory syntax, the default snapshots location and the three database paths. Removed the claim that metadata always stays in one directory and the closing recovery-guide sentence, which the page does not state.
Method: documentation only; no commands were run.
