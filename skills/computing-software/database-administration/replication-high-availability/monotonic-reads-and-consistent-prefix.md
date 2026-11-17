---
id: computing-software.database-administration.replication-high-availability.monotonic-reads-and-consistent-prefix
name: monotonic-reads-and-consistent-prefix
category: computing-software
field: database-administration
product: replication-high-availability
tags: [database-administration, replication-high-availability, monotonic-reads, consistent-prefix, read-your-writes, replication-lag, consistency-models]
level: practitioner
status: draft
description: "Prevent replication-lag anomalies for users: read-your-writes, monotonic reads and consistent prefix reads, with routing patterns using LSN/GTID tracking and sticky replicas."
sources:
  - https://dataintensive.net/
  - https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-RECOVERY-CONTROL
  - https://dev.mysql.com/doc/refman/8.4/en/gtid-functions.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monotonic reads and consistent prefix reads

Async replicas lag; reads routed to different replicas can expose anomalies (Kleppmann, DDIA ch.5).

## The anomalies
| Guarantee | Violation |
|---|---|
| Read-your-writes | User saves a comment, reloads, it is gone (read hit a lagging replica) |
| Monotonic reads | User sees a comment, refreshes, it disappears (second read hit a more-lagged replica): time goes backwards |
| Consistent prefix | Observer sees an answer before the question (writes from different partitions/replicas arrive out of causal order) |

## Patterns
**Read-your-writes**
- Route the user's reads to the primary for N seconds after they write (simple, coarse).
- Track the commit position and wait for a replica to reach it:
  - PostgreSQL: after write, `SELECT pg_current_wal_lsn()`; on replica read, check `pg_last_wal_replay_lsn() >= :lsn`, otherwise wait briefly or go to primary.
  - MySQL: capture GTID (`session_track_gtids=OWN_GTID` returns it to the client); on replica `SELECT WAIT_FOR_EXECUTED_GTID_SET(:gtid, 1)`.
  - MongoDB: causally consistent sessions do this automatically (`afterClusterTime`).
  - ProxySQL GTID causal reads, AWS Aurora/RDS Proxy features implement it in the proxy layer.

**Monotonic reads**
- Pin each user/session to one replica (hash of user id → replica); fail over to another only with the same position check.
- Or carry the last-seen position in the session token and require replicas ≥ it.

**Consistent prefix**
- Keep causally related writes in the same partition/shard (single leader orders them).
- Use causal tokens / version vectors across partitions when that is impossible.

## Measure first
Lag distribution matters: `pg_stat_replication.replay_lag`, MySQL `Seconds_Behind_Source` (coarse) or heartbeat tables (pt-heartbeat), MongoDB `rs.printSecondaryReplicationInfo()`.

## Verify
Test harness: write then immediately read through the routing layer 10,000 times under induced replica lag (pause replay: `pg_wal_replay_pause()`); zero stale reads for read-your-writes paths.
