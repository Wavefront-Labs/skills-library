---
id: computing-software.cloud-infrastructure-engineering.garage.metadata-db-engine-selection
name: metadata-db-engine-selection
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [db-engine, lmdb, sqlite, fjall]
level: advanced
status: docs-checked
description: "Pick lmdb, sqlite or fjall for db_engine and know the corruption, portability and key-size limits of LMDB."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`db_engine` selects the metadata store:

| engine | value | path |
|---|---|---|
| LMDB (default since v0.9.0) | `"lmdb"` | `<metadata_dir>/db.lmdb/` |
| Sqlite | `"sqlite"` | `<metadata_dir>/db.sqlite` |
| Fjall (experimental) | `"fjall"` | `<metadata_dir>/db.fjall/` |
| Sled | removed in v1.0 | |

LMDB is recommended for high-performance clusters with `replication_factor` of 2 or more. Its limitations: it is prone to corruption after an unclean shutdown such as a kill or power loss, so configure `metadata_auto_snapshot_interval`; its format is not portable between architectures (x86-64 to ARM64 will not work); 32-bit systems get tiny database sizes; and keys are limited to 511 bytes, which means S3 object keys and K2V sort keys are limited to 479 bytes.

Sqlite avoids those problems but is slower. It always runs in WAL mode.

Fjall is an LSM-tree engine that may raise write throughput, but support is experimental, added for evaluation only. Use it with test data only.

To convert between engines, give full database paths, not just the metadata directory:

`garage convert-db -a <input engine> -i <input path> -b <output engine> -o <output path>`

## Checked

2026-11-04. Read the Configuration file format page in full. Confirmed the engine table with paths and versions, the LMDB recommendation and its four limitations, Sqlite WAL mode, the experimental Fjall warning and the convert-db syntax. Nothing removed.
Method: documentation only; no commands were run.
