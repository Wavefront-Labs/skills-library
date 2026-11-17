---
id: computing-software.database-administration.clickhouse.data-skipping-indexes
name: data-skipping-indexes
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, skip-index, minmax, bloom-filter, set-index]
level: practitioner
status: docs-checked
description: "Add ClickHouse data skipping indexes (minmax, set, bloom_filter, text) only after key design and verify them with EXPLAIN indexes=1."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/using_data_skipping_indices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# data skipping indexes
Skip indexes let ClickHouse avoid reading blocks of data guaranteed not to match a filter, which helps when the primary key does not. They store metadata per block (min/max, value sets or Bloom filters), apply only to the MergeTree family, and are defined by an expression, type, name and a granularity that sets the size of each indexed block. Types on the page:
- `minmax`: min and max per block; ideal for range queries on loosely sorted data.
- `set(N)`: up to N values per block; effective on columns with low cardinality per block.
- `text`: inverted index over tokenised strings for deterministic full-text search; preferred over approximate Bloom-filter approaches.
- `bloom_filter`: probabilistic membership; for "needle in a haystack" lookups.
- `tokenbf_v1` / `ngrambf_v1`: deprecated in ClickHouse 26.2 and later in favour of text indexes.

Add after the table exists, then materialize (the page's example):
```sql
ALTER TABLE stackoverflow.posts
  (ADD INDEX view_count_idx ViewCount TYPE minmax GRANULARITY 1);

ALTER TABLE stackoverflow.posts MATERIALIZE INDEX view_count_idx;
```
Or define it in `CREATE TABLE`: `INDEX view_count_idx ViewCount TYPE minmax GRANULARITY 1`.

Guidance from the page:
- Use them after types, primary key and materialized views are right. They only help if they eliminate many blocks; one matching value forces the whole block to be read, so a strong correlation between the indexed column and the primary key (or inserts that group similar values) matters.
- Good for columns with high overall cardinality but low cardinality within a block, rare critical values (error codes, specific IDs), and filters on non-key columns with localised distribution.
- Test on real data with realistic queries and try different types and granularity values. Check index size: smaller granularity filters more granules but grows the index and can degrade performance, especially for bloom filters.
- Check effect with `EXPLAIN indexes = 1` or `send_logs_level='trace'`.

Docs example: `ViewCount` correlates with `CreationDate` (in the key), so a minmax index on it cut `EXPLAIN` granules for `ViewCount > 10000000` from 8513 to a `Skip` entry of `Granules: 23/8513` and rows read from 59.55 million to 39.11 thousand. The `Skip` section lists the index name, description and parts/granules selected.

## Checked
2026-11-03. Confirmed against the "Use data skipping indices where appropriate" page. Removed: the `set(100) GRANULARITY 4` example on an invented `logs` table, the claim that `ADD INDEX` affects only new parts (not stated), the "(confirm for your version)" marker (the page says 26.2 and later) and the uncorrelated-random-column gotcha as worded.
Method: documentation only; no commands were run.
