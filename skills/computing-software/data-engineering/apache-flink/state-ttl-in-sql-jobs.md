---
id: computing-software.data-engineering.apache-flink.state-ttl-in-sql-jobs
name: state-ttl-in-sql-jobs
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink-sql, table-exec-state-ttl, state-ttl-hint, regular-join, unbounded-state, state-ttl, compiled-plan]
level: advanced
status: gated
description: "Bound state in Flink SQL jobs: table.exec.state.ttl, per-operator STATE_TTL hints, which operators need it (regular joins, group aggs, dedup), and correctness trade-offs."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/config/#table-exec-state-ttl
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/sql/queries/hints/#state-ttl-hints
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/concepts/overview/#idle-state-retention-time
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State TTL in Flink SQL jobs

**Goal:** stop unbounded state growth from regular joins and non-windowed aggregations, without silently producing wrong results.

## Which operators keep state forever
- Regular (non-windowed, non-interval) **joins**: both sides retained indefinitely.
- Non-windowed `GROUP BY` aggregations: one accumulator per key forever.
- Deduplication and Top-N on unbounded keys.
- `DISTINCT` aggregates.
Windowed aggregations, window joins, interval joins and temporal joins clean up via watermarks and do **not** need TTL.

## Global TTL
```sql
SET 'table.exec.state.ttl' = '36 h';
```
State for a key not accessed for 36 h is dropped. Default 0 = never.

## Per-operator TTL hints
```sql
SELECT /*+ STATE_TTL('o' = '1d', 'p' = '30d') */ o.order_id, p.status
FROM orders o
JOIN payments p ON o.order_id = p.order_id;

SELECT /*+ STATE_TTL('orders' = '7d') */ customer_id, COUNT(*) FROM orders GROUP BY customer_id;
```
Lets the fast-moving side expire quickly while keeping the dimension-like side longer. Hints take precedence over the global value. For more control, compile a plan (`COMPILE PLAN`) and edit per-operator TTL in the JSON plan. (gated: unconfirmed, source is paywalled or blocked)

## Correctness consequences
- Join: a payment arriving after the order's state expired finds no match: inner join emits nothing; left join emits a null-padded row. Choose TTL > maximum realistic gap between matching events.
- Group aggregation: a key reappearing after expiry restarts from zero; the sink receives a new row (or overwrites the old total in an upsert sink, which is then wrong). Use TTL only for keys that truly go cold (sessions, orders) or use windowed aggregation.
- Prefer **interval joins** (`o.ts BETWEEN p.ts - INTERVAL '1' HOUR AND p.ts`) or temporal joins when the relationship has a time bound.

## Monitoring
- Checkpoint size per operator (Web UI checkpoint details) should plateau after TTL is reached.

## Gotchas
- TTL is processing time based (wall clock of last access), not event time.
- Changing TTL on an existing job: restored state keeps its old timestamps; works, but changing from 0 to N only expires after N of inactivity from restore.
- Lookup joins keep no state (they query the external table); caching options control staleness instead.

## Verify
- [ ] Every regular join/group agg in the job has an intentional TTL (global or hint).
- [ ] Checkpoint size growth flattens after the TTL horizon.

## Checked

2026-10-28. Confirmed: table.exec.state.ttl and its default (never clean up) on the table config page. Removed: an RocksDB metric key and a version gate; the STATE_TTL hint page returned a stub, so that claim is gated.

Method: documentation only; no commands were run.
