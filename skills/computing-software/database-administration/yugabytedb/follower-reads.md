---
id: computing-software.database-administration.yugabytedb.follower-reads
name: follower-reads
category: computing-software
field: database-administration
product: yugabytedb
tags: [follower-reads, read-replicas, staleness, yb-follower-read-staleness-ms, max-stale-read-bound-time-ms, latency]
level: practitioner
status: docs-checked
description: "Serve reads from the nearest replica with follower reads, set staleness bounds in YSQL, and understand when a follower rejects a read and falls back to the leader."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/additional-features/follower-reads.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Follower reads

Normally a read goes to the tablet leader. Follower reads serve it from the closest replica for lower latency, at the cost of slightly stale data. Writes still go to the leader.

YSQL: a read uses a follower only when `yb_read_from_followers` is true (default false) and the transaction or session is read only; set it per session or per transaction with `SET LOCAL` before the first statement. A follower read executes at one consistent time, now minus `yb_follower_read_staleness_ms` (default 30 seconds; the value must be at least twice `--max_clock_skew_usec`, so 1000 ms minimum with the default). YCQL has no staleness setting; the follower answers at its safe time, so the result is as old as the follower's lag.

A follower may reject a read and make the client retry at the leader:
- Too far behind: its safe time is older than now minus `--max_stale_read_bound_time_ms` (default 60 seconds). Raise the flag if followers far from the leader fall here too often; 0 turns the check off.
- YSQL only: it lacks all data at the read time. With `--ysql_follower_reads_avoid_waiting_for_safe_time=true` (the default) it rejects; with false it waits to catch up.
- Otherwise it serves the read. A rejected read is always retried at the tablet leader, not at another follower; the `consistent_prefix_failed_reads` metric counts these retries.

YCQL follower reads need consistency level ONE; LOCAL_ONE and the default QUORUM read from the leader. A read replica cluster serves reads only as follower reads; with follower reads off, the read goes to the leader in the primary cluster. Pair follower reads with a staleness value larger than typical replication lag so most reads are accepted locally.

## Checked

2026-11-04. Confirmed against the Follower reads page: leader vs closest replica, timeline-consistent stale reads, YSQL read time (now minus `yb_follower_read_staleness_ms`), YCQL safe time, `--max_stale_read_bound_time_ms` default 60 seconds with 0 disabling the check, the avoid-waiting flag default true, retries at the leader, `yb_read_from_followers` default false, YCQL consistency ONE, and read replica behaviour. Replaced the shorthand `avoid_waiting` with the flag name the page gives. Removed nothing.

Method: documentation only; no commands were run.
