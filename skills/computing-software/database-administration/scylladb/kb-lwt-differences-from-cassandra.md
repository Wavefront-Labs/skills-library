---
id: computing-software.database-administration.scylladb.kb-lwt-differences-from-cassandra
name: kb-lwt-differences-from-cassandra
category: computing-software
field: database-administration
product: scylladb
tags: [lwt, lightweight-transactions, paxos, conditional-updates, batch]
level: advanced
status: docs-checked
description: "How ScyllaDB lightweight transactions differ from Cassandra: fewer rounds, synchronous commit log, stable result set, batch result order, mixed IF conditions, no hints."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/lwt-differences.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ScyllaDB LWT versus Cassandra

ScyllaDB aims for Cassandra compatibility, but lightweight transactions differ:
- Fewer rounds: the old row read is piggybacked on the Paxos response rather than a separate read query.
- Durability: LWT writes automatically use synchronous commit log mode, so data has hit the device before the transaction completes.
- Result set: metadata does not change between executions; ScyllaDB always returns the old version of the row whether or not the condition applied.
- Batches: the result contains an old row for every conditional statement, in statement order (Cassandra uses clustering key order). `IF EXISTS`, `IF NOT EXISTS` and other conditions may be mixed for the same row.
- Per-core partitioning: the RPC goes straight to the right core on the peer replica, avoiding concurrency overhead (when ScyllaDB's shard-aware driver is used; otherwise there is an extra hop at the coordinator).
- No hints: LWT writes are not hinted since they are already recorded in the `system.paxos` table.
- Arithmetic SET: `col = col + value` and `col = col - value` work on non-counter numeric columns in a conditional UPDATE (a ScyllaDB extension; Cassandra raises `InvalidRequest`).

Arithmetic details: an `IF` clause is mandatory, otherwise the statement is rejected. A null column stays null after arithmetic, so test with `IF score != null` rather than `IF EXISTS` to catch uninitialised values.

```
INSERT INTO mytable (pk, ck, score) VALUES (1, 1, 0) IF NOT EXISTS;
UPDATE mytable SET score = score + 1 WHERE pk = 1 AND ck = 1 IF EXISTS;
```

## Checked

2026-11-04. Confirmed against kb/lwt-differences.rst: every bullet, arithmetic SET rules and the null note. Added the shard-aware driver condition. Removed the monitoring advice about system.paxos, which the page does not give.

Method: documentation only; no commands were run.
