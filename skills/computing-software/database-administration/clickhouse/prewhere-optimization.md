---
id: computing-software.database-administration.clickhouse.prewhere-optimization
name: prewhere-optimization
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, prewhere, filtering, io-reduction, optimize-move-to-prewhere]
level: practitioner
status: docs-checked
description: "Reduce ClickHouse I/O with PREWHERE, which filters column by column before reading other columns; measure it with optimize_move_to_prewhere."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/best-practices/prewhere.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# prewhere optimization
PREWHERE is a query execution optimisation that filters out irrelevant data before reading non-filter columns. Without it, ClickHouse uses the primary index to pick granules, loads those granules (and aligned granules of every other needed column), then applies the remaining filters. With PREWHERE it filters column by column, loading at each step only granules that contain at least one row that survived the previous filter, so I/O and memory drop, especially on wide tables. It reduces data read, not rows processed.

You rarely need to write it: when `optimize_move_to_prewhere` is enabled (default true), ClickHouse moves filter conditions from WHERE to PREWHERE, prioritising those that reduce read volume most. Smaller columns go first: as of 23.2 PREWHERE filter columns are sorted by ascending uncompressed size, and from 23.11 optional column statistics can order them by actual selectivity.

Manual syntax:
```sql
SELECT street, price
FROM uk_price_paid_simple
PREWHERE town = 'LONDON'
WHERE date >= '2024-01-01';
```
Measure the effect by running the same query with `SETTINGS optimize_move_to_prewhere = false` and `= true`. In the docs example both processed 2.31 million rows, but read 23.36 MB without and 6.74 MB with PREWHERE, about three times faster. Inspect it with `EXPLAIN PLAN actions = 1` (look for `Prewhere info`) or `SETTINGS send_logs_level = 'test'`, which logs "Condition ... moved to PREWHERE" and each PREWHERE step.

## Checked
2026-11-03. Confirmed against the "How does the PREWHERE optimization work?" page. Removed: the claim that it is MergeTree-only, the FINAL caveat, the "cheap" wording, and the `read_bytes` Verify step, none of which are on the page.
Method: documentation only; no commands were run.
