---
id: computing-software.database-administration.clickhouse.query-parallelism-max-threads
name: query-parallelism-max-threads
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, max-threads, parallelism, processing-lanes, trace-logs]
level: practitioner
status: docs-checked
description: "How ClickHouse parallelises a query across processing lanes set by max_threads, and why it can use fewer; inspect with EXPLAIN PIPELINE."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/best-practices/query-parallelism.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# query parallelism max threads
For an aggregation with a filter on the primary key, ClickHouse loads the primary index to identify which granules to process, then distributes them dynamically across `n` parallel processing lanes that stream and process data block by block. `n` is the `max_threads` setting, which by default matches the number of cores available to ClickHouse on the server (59 on the docs' test server, readable with `SELECT getSetting('max_threads')`). On a machine with twice the cores, throughput roughly doubles but memory use also increases. `Resize` operators in the plan rebalance blocks across lanes so faster lanes help slower ones.

On sharded tables each server processes its shard with its own lanes, and the server that received the query combines the sub-results. In ClickHouse Cloud, parallel replicas play the role of shards.

`max_threads` is an upper limit, not a guaranteed count: extra lanes are allocated only when there is enough data. Which is "enough" is mainly set by the minimum rows (163,840 default) and bytes (2,097,152 default) each lane should handle: `merge_tree_min_rows_for_concurrent_read` and `merge_tree_min_bytes_for_concurrent_read` (the `..._for_remote_filesystem` variants for shared storage such as Cloud). In the docs, a `WHERE town = 'LONDON'` query selected 282 of 3,609 granules and used only 30 streams despite `max_threads` 59. The docs warn against changing those settings in production.

Inspect lane usage with trace logs and `EXPLAIN PIPELINE`:
```sql
SELECT max(price) FROM uk.uk_price_paid_simple
SETTINGS send_logs_level='trace';

EXPLAIN PIPELINE
SELECT max(price) FROM uk.uk_price_paid_simple;
```
The trace shows e.g. "Reading approx. 29564928 rows with 59 streams"; in the pipeline, operators marked `× 59` run concurrently on non-overlapping data regions. `EXPLAIN indexes = 1` shows how many granules the primary index selected.

## Checked
2026-11-03. Confirmed against the "How ClickHouse executes a query in parallel" page. Removed: the `SET max_threads = 8` snippet, `system.query_log` ProfileEvents CPU check, the "selective filter or serial work" diagnosis, and the starve/cap-per-profile gotcha and the two-value timing Verify step, none of which are on the page.
Method: documentation only; no commands were run.
