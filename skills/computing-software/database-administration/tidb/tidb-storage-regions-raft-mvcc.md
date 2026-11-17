---
id: computing-software.database-administration.tidb.tidb-storage-regions-raft-mvcc
name: tidb-storage-regions-raft-mvcc
category: computing-software
field: database-administration
product: tidb
tags: [tidb, tikv, region, raft, rocksdb, mvcc, percolator, key-value, replication]
level: advanced
status: docs-checked
description: "Understand how TiKV stores data: ordered key-value space on RocksDB, range-split Regions replicated by Raft, MVCC versioned keys and Percolator transactions."
sources: ["https://docs.pingcap.com/tidb/stable/tidb-storage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb storage regions raft mvcc

TiKV treats storage as one huge ordered map of key-value pairs, sorted by binary key order, so you can seek to a key and iterate forward. This model is independent of SQL tables.

Layers:
- Local engine: data is written to RocksDB rather than raw disk, because building a single-node engine is costly.
- Raft: each data change is a Raft log entry replicated across the Raft group; a write succeeds once a majority of nodes have it. Raft provides leader election, membership changes (add or remove replicas, transfer leader) and log replication. Writes go through the Raft interface, not directly to RocksDB.
- Regions: TiKV chooses range partitioning, not hashing. The key space is split into consecutive `[StartKey, EndKey)` segments called Regions; the default size limit is 256 MiB and is configurable. PD spreads Regions evenly across nodes, which gives horizontal scalability and load balancing, and keeps a record of which node holds which Region. Replicas of a Region form a Raft group with one Leader; by default reads and writes are served by the Leader.
- MVCC: versions are appended to keys (`Key_Version`), with larger versions ordered first, so a reader at an earlier logical time can read the old value while a writer proceeds. This avoids read/write blocking and deadlock in a distributed setting.
- Transactions: the model follows Google's Percolator paper, with optimizations.

A Region is unrelated to a SQL table: the storage layer is described purely in key-value terms.

## Checked

2026-11-09: all claims confirmed against the TiDB Storage page (pingcap/docs tidb-storage.md, read in full). Removed the unsourced statement about how tables map onto Regions.

Method: docs-checked 2026-11-09 against pingcap/docs tidb-storage.md
