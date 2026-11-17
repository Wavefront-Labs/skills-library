---
id: computing-software.database-administration.cockroachdb.follower-reads
name: follower-reads
category: computing-software
field: database-administration
product: cockroachdb
tags: [follower-reads, stale-reads, as-of-system-time, bounded-staleness, global-tables]
level: practitioner
status: docs-checked
description: "Serve reads from the nearest CockroachDB replica: strong reads on GLOBAL tables, exact staleness with follower_read_timestamp(), and bounded staleness."
sources:
  - https://www.cockroachlabs.com/docs/stable/follower-reads
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: cut read latency in multi-region clusters by reading from the nearest replica rather than the leaseholder.

Types:
- Strong follower read: a normal `SELECT` on a `GLOBAL` table (low-latency reads everywhere, higher write latency), or a long-running `SELECT` whose read timestamp has fallen behind the closed timestamp.
- Stale follower read: a historical read from the nearest replica; results may not reflect the latest writes but are always a consistent committed view.

Exact staleness: any `SELECT` with a suitable `AS OF SYSTEM TIME`. Use the convenience function:
```sql
SELECT ... FROM ... AS OF SYSTEM TIME follower_read_timestamp();
SELECT now() - follower_read_timestamp();   -- see the current offset
BEGIN;
SET TRANSACTION AS OF SYSTEM TIME follower_read_timestamp();
SELECT ...; COMMIT;
```
Choose it when you need multi-statement reads in a transaction and can tolerate data at least about 4.2 seconds old. The timestamp must be far enough in the past or the read may block on a conflicting write and not be served locally.

Bounded staleness reads compute a dynamic, system-chosen timestamp (via `with_min_timestamp` or `with_max_staleness`), tolerate replication lag better, and stay available during partitions, at slightly higher cost.

Limits: follower reads are read-only; you cannot use them in read-write transactions.

## Checked

2026-11-03. Confirmed against the follower reads page: strong and stale follower reads, `follower_read_timestamp()`, 4.2 second staleness, bounded staleness functions, read-only limit. Removed: unsupported `EXPLAIN ANALYZE` cross-region verification.
Method: documentation only; no commands were run.
