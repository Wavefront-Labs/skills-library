---
id: computing-software.database-administration.clickhouse.selecting-insert-strategy-and-format
name: selecting-insert-strategy-and-format
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, insert, strategy, batch, formats, native, compression]
level: practitioner
status: docs-checked
description: "Choose how to push data into ClickHouse: batching, input format, compression, pre-sorting, insert target and native vs HTTP interface."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/selecting_an_insert_strategy.md
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/_snippets/_bulk_inserts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# selecting insert strategy and format
Inserts are synchronous by default: each one immediately creates a part on disk. Use synchronous inserts if you can batch client-side (at least 1,000 rows, ideally 10,000-100,000; about one insert query per second); otherwise use asynchronous inserts (see async-inserts-and-batching). For pulling data in with table functions such as `s3` and `gcs`, the page points to a separate S3 guide.

Retries: MergeTree deduplicates inserts by default, so retrying after an ambiguous failure is safe as long as batch contents and order are identical.

Insert target on sharded clusters: insert directly into a MergeTree or ReplicatedMergeTree table (most efficient when the client load-balances; with `internal_replication = true` ClickHouse handles replication), or into a Distributed table (simpler, slightly slower because of forwarding; `internal_replication = true` still recommended). In ClickHouse Cloud inserts are balanced across nodes automatically.

Format (70+ supported): Native is recommended and most efficient (default in the Go and Python clients); RowBinary is efficient row-based (Java client); JSONEachRow is easy but expensive to parse, for low volume.

Compression: LZ4 is fast and the default in most clients; ZSTD compresses more but costs more CPU, worth it when bandwidth is constrained or egress is costly. Over the native interface LZ4 is on by default; over HTTP use a header such as `Content-Encoding: lz4` and compress the entire payload.

Pre-sorting by primary key can skip the server-side sort and help compression, but is optional; the page recommends it only if data is nearly ordered or client resources are underused.

Interfaces: native (clickhouse-client, Go, C++) always sends Native format, compresses block-wise and can compute MATERIALIZED and DEFAULT values client-side; HTTP takes any format, is easier to load balance, with slightly more overhead.

## Checked
2026-11-03. Confirmed against the "Selecting an insert strategy" page and its bulk-insert snippet. Removed: the "insert deduplication tokens" advice, the `INSERT ... SELECT`/s3/url loading bullet, the inline async INSERT example, the "async can lose data on crash" gotcha wording and the Verify step (`system.asynchronous_insert_log` is not the table the docs name).
Method: documentation only; no commands were run.
