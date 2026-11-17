---
id: computing-software.cloud-infrastructure-engineering.garage.metadata-and-data-fsync
name: metadata-and-data-fsync
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [metadata-fsync, data-fsync, durability, power-loss]
level: advanced
status: docs-checked
description: "Trade write speed for crash safety with metadata_fsync and data_fsync, both off by default."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`metadata_fsync` enables synchronous mode in the database engine. It is `false` by default. Turning it on lowers the risk of metadata corruption after power failure, at a significant cost in write performance, because Garage must pause to sync several times for calls such as PutObject. It also reduces the chance of simultaneous corruption on several nodes, which could lose data. With multi-site replication it is probably unnecessary, since two sites rarely lose power at the same instant, and a corrupted file on one node can be deleted and rebuilt from the others.

Effect per engine:

- Sqlite: `PRAGMA synchronous = OFF` becomes `NORMAL`.
- LMDB: `MDB_NOMETASYNC + MDB_NOSYNC` becomes just `MDB_NOMETASYNC`.
- Fjall: no change, the option is not supported.

`data_fsync` also defaults to `false`. When true, Garage fsyncs each data block and its containing directory after saving it. This reduces the risk of losing a block when several nodes lose power together, for a moderate write slowdown, and like the metadata option it is likely unnecessary with geographical replication.

## Checked

2026-11-04. Read the Configuration file format page in full. Confirmed both defaults, the performance trade-offs, the multi-site remark and the per-engine table. Nothing removed.
Method: documentation only; no commands were run.
