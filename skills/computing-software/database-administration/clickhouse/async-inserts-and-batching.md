---
id: computing-software.database-administration.clickhouse.async-inserts-and-batching
name: async-inserts-and-batching
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, async-insert, batching, wait-for-async-insert, too-many-parts]
level: practitioner
status: docs-checked
description: "Prevent too-many-parts by batching inserts client-side or enabling ClickHouse async_insert with its flush thresholds and wait mode."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/selecting_an_insert_strategy.md
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/_snippets/_async_inserts.md
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/_snippets/_bulk_inserts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# async inserts and batching
Synchronous inserts (the default) create a storage part per insert, so many small ones cause poor query performance and "too many parts" errors. The docs recommend client-side batches of at least 1,000 rows, ideally 10,000-100,000, and about one insert query per second so background merges keep up. When client batching is not feasible (e.g. thousands of agents sending small payloads), use asynchronous inserts: the server buffers data in memory and flushes it by thresholds. They work over HTTP and native TCP.

Enable for a user, a query, or as a client connection parameter:
```sql
ALTER USER default SETTINGS async_insert = 1
INSERT INTO YourTable SETTINGS async_insert=1, wait_for_async_insert=1 VALUES (...)
```
With `async_insert = 1`, data is written when the first of these is reached:
- `async_insert_max_data_size` (default 100 MiB)
- `async_insert_busy_timeout_ms` (default 200 ms, or 1000 ms on Cloud)
- `async_insert_max_query_number` (default 450)

Since 24.2 the flush timeout is adaptive (`async_insert_use_adaptive_busy_timeout`), moving between `async_insert_busy_timeout_min_ms` (default 50 ms) and the max.

Return modes: `wait_for_async_insert = 1` (default) acknowledges only after the flush to disk and returns flush errors to the client; the docs strongly recommend `async_insert=1, wait_for_async_insert=1`. `wait_for_async_insert = 0` is fire-and-forget: no persistence guarantee, errors only at flush, no dead-letter queue, and the client may keep writing when the server needs backpressure.

Behaviour: buffered data cannot be queried until flushed; there are multiple buffers per insert shape and settings combination, and per node in a cluster. Parsing and schema validation happen at flush, and one bad row rejects the whole query's payload; in fire-and-forget mode errors go to server logs and `system.asynchronous_inserts`. Each flush creates at least one part per partition key value, so a high-cardinality partition key can still give "too many parts". Deduplication is disabled for async inserts unless enabled explicitly (not with dependent materialized views). `INSERT INTO ... SELECT` is always synchronous. `SYSTEM FLUSH ASYNC INSERT QUEUE` flushes all buffers, e.g. before shutdown.

## Checked
2026-11-03. Confirmed against the "Selecting an insert strategy" page and the async and bulk-insert snippets it includes. Fixed: the skill pointed at `system.asynchronous_insert_log`, but the page names `system.asynchronous_inserts`; batch size was "thousands to hundreds of thousands", the page says at least 1,000, ideally 10,000-100,000. Removed: the `INSERT INTO logs ... VALUES (now(), ...)` example, the part-count Verify step and the retry-deduplication cross-reference wording.
Method: documentation only; no commands were run.
