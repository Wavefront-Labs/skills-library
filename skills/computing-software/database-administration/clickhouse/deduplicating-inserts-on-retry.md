---
id: computing-software.database-administration.clickhouse.deduplicating-inserts-on-retry
name: deduplicating-inserts-on-retry
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, deduplication, insert-deduplicate, retries, replicated]
level: practitioner
status: docs-checked
description: "Make ClickHouse insert retries idempotent using block-level deduplication, identical batches and insert_deduplication_token."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/developer/deduplicating-inserts-on-retries.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# deduplicating inserts on retry
Retrying a timed-out INSERT can write the same rows twice. ClickHouse can deduplicate inserted blocks: replicated MergeTree tables keep checksums of recent inserted blocks and skip a block whose checksum was already inserted; only *MergeTree engines support it; non-replicated tables use `non_replicated_deduplication_window`.

Conditions for a retry to be deduplicated:
- the retry sends the same data in the same order (the deduplication key is a block hash of the inserted data);
- `insert_deduplicate` is on (default for replicated tables);
- the original block is still within `replicated_deduplication_window`.

You can supply your own idempotency key:
```sql
INSERT INTO events SETTINGS insert_deduplication_token = 'batch-2026-11-03-0001'
VALUES (...);
```
Use a unique token per logical batch and reuse it on retry.

Materialized views: when deduplication is enabled for the source and `deduplicate_blocks_in_dependent_materialized_views` is set, dependent views also skip duplicates (the guide says to also enable that setting).

Gotchas: data inserted with `insert_deduplicate=0` cannot be deduplicated later; `insert_deduplication_token` takes priority over the data hash.

## Checked
2026-11-03. Confirmed against the ClickHouse docs guide "Deduplicating inserts on retries": default-on for *ReplicatedMergeTree with `replicated_deduplication_window`, `non_replicated_deduplication_window`, `insert_deduplicate`, `insert_deduplication_token` and its priority, `deduplicate_blocks_in_dependent_materialized_views`. Removed: the `max_insert_block_size` condition, the finite-window and ReplacingMergeTree gotchas and the part_log Verify step.
Method: documentation only; no commands were run.
