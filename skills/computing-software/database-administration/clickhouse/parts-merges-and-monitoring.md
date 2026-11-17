---
id: computing-software.database-administration.clickhouse.parts-merges-and-monitoring
name: parts-merges-and-monitoring
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, data-parts, merges, system-parts, merge-level]
level: practitioner
status: docs-checked
description: "How ClickHouse MergeTree inserts create immutable parts that background merges combine, and how to read merge level in system.parts."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/managing-data/core-concepts/merges.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# parts merges and monitoring
Inserts into MergeTree-family tables create sorted, immutable data parts; all data processing is offloaded to background merges. ClickHouse continuously merges smaller parts into larger ones per partition until they reach a compressed size of approximately 150 GB. Each merge increments the part's merge level by one; level 0 is a new, unmerged part. Merged-away parts are marked inactive and deleted after a configurable time (8 minutes by default).

Merge mechanics: the compressed column files of the source parts are decompressed and loaded, merged into larger column files, a new sparse primary index is generated, and the result is compressed and written to a new directory. What step two does depends on the engine: ReplacingMergeTree keeps only the most recent row per sorting key, SummingMergeTree sums numeric columns of rows with the same sorting key, AggregatingMergeTree stores partial aggregation states. Vertical merging loads and merges parts in chunks of blocks to reduce memory at the cost of merge speed. A server runs several background merge threads concurrently; more CPU cores and RAM raise merge throughput.

Monitor parts:
```sql
SELECT name, level, rows
FROM system.parts
WHERE (database = 'uk') AND (`table` = 'uk_price_paid_simple') AND active
ORDER BY name ASC;
```
In the docs example four active level-1 parts (`all_0_5_1`, `all_12_17_1`, `all_18_23_1`, `all_6_11_1`) later merged into a single `all_0_23_2` at level 2 with 25,248,433 rows. ClickHouse 24.10 added a merges dashboard to the built-in dashboards, available in OSS and Cloud via the `/merges` HTTP handler.

## Checked
2026-11-03. Confirmed against the "Part merges" page. Removed: part-name decoding wording, the claim to prefer larger inserts over merge threads, `system.merges` and `system.part_log`, the `OPTIMIZE ... FINAL` gotcha and the Verify step, none of which are on the page.
Method: documentation only; no commands were run.
