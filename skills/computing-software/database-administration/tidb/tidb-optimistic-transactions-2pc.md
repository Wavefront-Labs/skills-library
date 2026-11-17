---
id: computing-software.database-administration.tidb.tidb-optimistic-transactions-2pc
name: tidb-optimistic-transactions-2pc
category: computing-software
field: database-administration
product: tidb
tags: [tidb, optimistic-transaction, two-phase-commit, prewrite, commit, start-ts, write-conflict, percolator]
level: advanced
status: docs-checked
description: "Know how TiDB optimistic transactions detect conflicts at commit with two-phase commit, and why COMMIT can fail so applications must handle it."
sources: ["https://docs.pingcap.com/tidb/stable/optimistic-transaction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb optimistic transactions 2pc

In optimistic mode conflicts are found at commit time. This skips row-lock acquisition and helps when concurrent transactions rarely touch the same rows. The cost: `COMMIT` can return an error, so make sure the application handles it. If unsure, use pessimistic transactions instead. Since v3.0.8 new clusters default to pessimistic mode.

Two-phase commit flow in TiDB:
1. `BEGIN`: TiDB gets a globally unique, monotonic timestamp from PD as `start_ts`; it also serves as the snapshot version.
2. Reads get routing from PD and read the `start_ts` version from TiKV.
3. Writes are checked against constraints (data types, NOT NULL) and held in the transaction's private memory in TiDB.
4. On `COMMIT`, TiDB starts 2PC: it selects a primary key, gets Region distribution from PD and groups keys by Region.
5. Prewrite: TiDB sends prewrite requests to all involved TiKV nodes; TiKV checks for conflicts or expired versions and locks valid data.
6. After all prewrites succeed, TiDB gets `commit_ts` from PD and commits the primary key, which clears its prewrite lock; then the success is returned to the client and TiDB asynchronously cleans the remaining locks.

Advantages: simple, cross-node transactions built on single-row transactions, decentralized lock management. Disadvantages: 2PC latency, dependence on a central timestamp allocator, and possible OOM when a lot of data is buffered in memory.

Write-write conflicts in heavy contention make commits fail. Starting from v8.0.0, `tidb_disable_txn_auto_retry` is deprecated and TiDB no longer automatically retries optimistic transactions, so retry in the application or use pessimistic mode.

Choose optimistic mode only for low-contention workloads with retry logic.

## Checked

2026-11-09: warning about COMMIT errors, pessimistic default, the 2PC steps, advantages and disadvantages and the v8.0.0 retry change confirmed against the TiDB Optimistic Transaction Model page (pingcap/docs optimistic-transaction.md, read in full).

Method: docs-checked 2026-11-09 against pingcap/docs optimistic-transaction.md
