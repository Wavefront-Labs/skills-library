---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.choosing-filer-store
name: choosing-filer-store
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [leveldb, redis2, cassandra, super-large-directory, filer-store, redis]
level: practitioner
status: docs-checked
description: "Pick a filer metadata store: embedded leveldb default versus Redis, Cassandra, SQL and others, with tombstone and super-large-directory trade-offs."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Filer-Stores
  - https://github.com/seaweedfs/seaweedfs/wiki/Choosing-a-Filer-Store
  - https://github.com/seaweedfs/seaweedfs/wiki/Super-Large-Directories
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# choosing filer store

The filer store holds only metadata (directories, entries, chunk file ids); file content stays on volume servers.

Highlights from the comparison table:
- `leveldb` / `leveldb2`: embedded, default, very fast; `leveldb3` keeps one instance per bucket.
- `rocksdb`, `sqlite`, `ydb`: need a manual build.
- `redis2`: one directory's children in one key (limited count); `redis3` spreads them (unlimited). Both have native TTL.
- `cassandra`, `mysql`, `mongodb`, `arangodb` and others: distributed, unlimited entries.

Stores are configured in `filer.toml`. Switching stores is possible; see the migration skill. Super large directories are set with the `superLargeDirectories` option in `filer.toml`; never change or remove entries there once configured, or data is lost, and the directory must start empty.

Gotchas:
- Cassandra/ScyllaDB use LSM storage: a directory with constant churn (e.g. a staging folder) accumulates tombstones and reads slow down. One user fixed that by moving the hot path to Redis (see the path-specific store skill).
- Super large directories (millions of direct children, e.g. one folder per user id) are implemented for Cassandra and Redis; the trade-off is that the direct children of such a directory cannot be listed, while deeper levels list normally.

Verify: after restart, create a file and read it back through the filer.

## Checked

Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Filer Stores (comparison table and switching section read), Choosing a Filer Store (read in full) and Super Large Directories (read in full). The scaffold command and log-line claims were removed as unconfirmed.
