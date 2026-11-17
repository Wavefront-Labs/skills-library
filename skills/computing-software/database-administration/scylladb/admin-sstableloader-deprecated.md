---
id: computing-software.database-administration.scylladb.admin-sstableloader-deprecated
name: admin-sstableloader-deprecated
category: computing-software
field: database-administration
product: scylladb
tags: [sstableloader, bulk-load, migration, cql, load-and-stream]
level: practitioner
status: docs-checked
description: "sstableloader (deprecated): bulk-load SSTable directories through the CQL API, directory-to-table naming, key options, Cassandra differences, encrypted and counter limits."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/admin-tools/sstableloader.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# sstableloader (deprecated)

Bulk loads SSTables from a directory into a ScyllaDB cluster over the **CQL API**. It is deprecated and will be removed; prefer `nodetool refresh --load-and-stream`. It differs from the Apache Cassandra tool of the same name, which uses an internal RPC protocol.

Limits:
- Cannot load encrypted files (see the Cassandra-to-ScyllaDB migration procedure for those).
- Local counters from Cassandra 2.0 cannot be migrated; ScyllaDB supports the global counters of Cassandra 2.1 and later.

Good for restoring ScyllaDB or Cassandra backups or cloning cluster to cluster, especially when node count or token distribution differ, since ScyllaDB distributes the data via CQL.

Usage: `sstableloader [options] <dir_path>`. The parent directories name the destination: to load `Standard1-g-1-Data.db` into `Keyspace1/Standard1`, put it with its `Standard1-g-1-Index.db` in a directory path ending `Keyspace1/Standard1/`.

Important options:
- `-d, --nodes <hosts>` (required): initial hosts, comma separated.
- `-p, --port` (default 9042); `--username` and `-pw`/`--password`: authentication user and password.
- `-cl, --consistency-level` (default ONE).
- `-j, --threads-count`, `-cph, --connections-per-host`: parallelism.
- `-nb, --no-batch`, `-bs, --batch-size`, `-nx, --no-prepared`.
- `-i, --ignore <nodes>`: do not stream to these nodes.
- `-g, --ignore-missing-columns`, `-ic, --ignore-dropped-counter-data`, `-ir, --no-infinite-retry`.
- TLS: `-ks`, `-kspw`, `-alg`, `-ciphers`, `-prtcl`, and `-f` pointing at a `cassandra.yaml`.

```
sstableloader -d 10.0.0.1,10.0.0.2 /path/to/Keyspace1/Standard1/
```

## Checked

2026-11-04: deprecation, Cassandra differences, encrypted-file and counter limits, usage, directory naming and the listed options confirmed against the ScyllaDB sstableloader documentation page. Fixed: authentication user option is `--username`, there is no `-u` on the page.

Method: documentation only; no commands were run.
