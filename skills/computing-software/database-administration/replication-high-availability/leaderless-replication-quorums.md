---
id: computing-software.database-administration.replication-high-availability.leaderless-replication-quorums
name: leaderless-replication-quorums
category: computing-software
field: database-administration
product: replication-high-availability
tags: [database-administration, replication-high-availability, leaderless-replication, read-repair, quorum, anti-entropy, hinted-handoff]
level: practitioner
status: docs-checked
description: "Operate leaderless (Dynamo-style) replication: N/W/R quorums, sloppy quorums and hinted handoff, read repair and anti-entropy repair, and the consistency limits."
sources:
  - https://dataintensive.net/
  - https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html
  - https://cassandra.apache.org/doc/latest/cassandra/managing/operating/repair.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Leaderless replication (quorums, read repair, anti-entropy)

Dynamo-style systems (for example Cassandra) let any replica accept writes; clients or coordinators send each operation to several replicas.

## Quorums
N = replicas per key, W = acks required for a write, R = replicas queried per read.
- `W + R > N` → read and write sets overlap: a read sees at least one copy of the latest acknowledged write (absent concurrency edge cases).
- Typical: N=3, W=2, R=2 (Cassandra `QUORUM`). `LOCAL_QUORUM` per datacentre for multi-region latency.
- Lower W/R → lower latency and higher availability, weaker freshness.

## Edge cases where quorums still return stale data
- Concurrent writes resolved by last-write-wins timestamps: clock skew silently drops writes.
- A write that succeeded on fewer than W replicas is reported failed but not rolled back.
- Sloppy quorums: during partitions, writes go to non-home nodes (**hinted handoff**), so `W + R > N` no longer guarantees overlap.
- Node restored from an old backup carries stale data until repaired.

## Read repair
On read, the coordinator compares responses; stale replicas are updated with the newest value. Works well for frequently read keys; rarely read data stays inconsistent.

## Anti-entropy repair
A background process compares replicas (Merkle trees) and streams differences. In Cassandra this is operator-driven:
```bash
nodetool repair -pr keyspace      # primary range per node, run on every node
```
Run it on a schedule on every node; read repair and hints are best-effort only.

## Hinted handoff
Coordinator stores writes for a down replica and replays when it returns (`max_hint_window`, default 3h). Longer outages require repair.

## Monitoring
Read repair rates, hints pending/dropped, repair completion per node, per-request consistency failures (unavailable and write-timeout errors).

## Verify
Repair schedule shows every token range repaired on schedule; chaos test (stop a node for longer than hint window, then repair) leaves no inconsistencies (`nodetool repair --validate` / compare checksums).

## Checked
2026-10-28. Confirmed in the Cassandra docs: R + W > N consistency model and `LOCAL_QUORUM` (guarantees page), best-effort read repair and hinted handoff, Merkle-tree anti-entropy repair, `max_hint_window` default 3h (cassandra.yaml reference), `nodetool repair -pr` and `--validate` (nodetool repair page). Removed: the `gc_grace_seconds` default and deadline claims, Cassandra Reaper and Scylla Manager, the Riak/ScyllaDB/DynamoDB list, and exception names not in the pages. The sloppy-quorum description rests on the book source, which was not read.
Method: documentation only; no commands were run.
