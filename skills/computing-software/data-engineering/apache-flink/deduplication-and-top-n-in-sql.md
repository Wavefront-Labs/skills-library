---
id: computing-software.data-engineering.apache-flink.deduplication-and-top-n-in-sql
name: deduplication-and-top-n-in-sql
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink-sql, top-n, deduplication, row-number, window-top-n, changelog, upsert]
level: practitioner
status: docs-checked
description: "Write Flink SQL deduplication and Top-N with ROW_NUMBER: keep-first vs keep-last semantics, window Top-N for append-only output, state cost and the changelog each produces."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/queries/deduplication/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/queries/topn/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/queries/window-topn/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/queries/window-deduplication/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/utility/explain/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deduplication and Top-N in Flink SQL

**Goal:** remove duplicate events and compute rankings in streaming SQL, with predictable state size and output type.

## Deduplication
Flink recognises this exact pattern (ROW_NUMBER over a time attribute, filter `= 1`):
```sql
-- keep FIRST event per order_id
SELECT order_id, customer_id, amount, order_time
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_time ASC) AS rn
  FROM orders)
WHERE rn = 1;

-- keep LAST event per order_id (ORDER BY ... DESC)
... ORDER BY order_time DESC ...
```
- Order by a **time attribute**: a processing-time attribute or an event-time (rowtime) attribute. `ASC` keeps the first row per key, `DESC` keeps the last.
- Check the changelog mode of the result with `EXPLAIN CHANGELOG_MODE` and make sure the sink can accept it; do not assume keep-last is append-only.
- State grows with distinct keys: set `table.exec.state.ttl` or use window deduplication.

## Window deduplication (bounded state, append-only)
```sql
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY window_start, window_end, order_id ORDER BY order_time) rn
  FROM TABLE(TUMBLE(TABLE orders, DESCRIPTOR(order_time), INTERVAL '1' HOUR)))
WHERE rn = 1;
```
Window deduplication emits only a final result at the end of the window (no intermediate results) and purges its intermediate state when no longer needed.

## Top-N (continuous)
```sql
SELECT category, product_id, sales
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC) AS rk
  FROM product_sales)          -- product_sales is itself an updating aggregate
WHERE rk <= 3;
```
The Top-N query is result-updating: when the top N records change, the changed ones are sent as retraction or update records. Omitting the rank column from the outer SELECT (the "no ranking output" optimization) can greatly reduce the records written to the result table, because the rank number is otherwise part of the unique key.

## Window Top-N (append-only)
```sql
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY window_start, window_end ORDER BY sales DESC) rk
  FROM (SELECT window_start, window_end, product_id, SUM(amount) sales
        FROM TABLE(TUMBLE(TABLE orders, DESCRIPTOR(order_time), INTERVAL '10' MINUTES))
        GROUP BY window_start, window_end, product_id))
WHERE rk <= 5;
```
Window Top-N emits only a final result per window, purges intermediate state, and needs `window_start` and `window_end` in the `PARTITION BY`.

## Gotchas
- The pattern must be followed exactly or the optimizer cannot translate the query; deduplication is the special case of Top-N with N = 1 ordered by a time attribute. Dedup requires `= 1`; a different filter or a non-time ordering column is a general Top-N.
- Unbounded keys without TTL: state grows forever; checkpoint sizes balloon.
- `EXPLAIN` the query with `CHANGELOG_MODE` and read the `changelogMode=[...]` of each node (for example `[I]` for insert-only, `[I,UA]` with updates).

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the Deduplication, Top-N, Window Deduplication, Window Top-N, Window TVF and EXPLAIN pages and the generated configuration table (`table.exec.state.ttl`): required `= 1` and `<= N` patterns, time-attribute ordering, ASC keeps first and DESC keeps last, result-updating Top-N, the no-ranking-output optimization, window variants emitting only final results, and `EXPLAIN CHANGELOG_MODE`. Removed unconfirmed claims about append-only keep-first output, named sink connectors and plan node names.

Method: documentation only; no commands were run.

## Verify
- [ ] `EXPLAIN CHANGELOG_MODE SELECT ...` shows the expected changelog mode for the sink.
- [ ] State size (checkpoint size per operator) stable over days.
