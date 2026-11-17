---
id: computing-software.database-administration.duckdb.duckdb-hive-partitioning-read
name: duckdb-hive-partitioning-read
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, hive-partitioning, hive-types, parquet, filter-pushdown]
level: practitioner
status: docs-checked
description: "Read Hive-partitioned datasets in DuckDB: hive_partitioning flag, auto-detection, partition filter pushdown, and hive_types casting."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/data/partitioning/hive_partitioning.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: query a `key=value` folder tree and have partition columns appear, with file pruning.

Layout example: `orders/year=2021/month=1/file1.parquet`, `orders/year=2022/month=11/file4.parquet`, and so on.

```sql
SELECT * FROM read_parquet('orders/*/*/*.parquet', hive_partitioning = true);
```
The `year` and `month` values come from the directory names. With `hive_partitioning = false` those columns are omitted:

```sql
FROM read_parquet('test/*/*/*.parquet', hive_partitioning = false);  -- no year, month columns
```

Filter pushdown: predicates on partition keys prune files, so `WHERE year = 2022 AND month = 11` reads only `orders/year=2022/month=11/*`.

Auto-detection: by default DuckDB inspects folder names for a `key=value` pattern and enables partitioning itself. Override session-wide with `SET hive_partitioning = false;` or per call with the parameter.

Types: `hive_types` specifies the logical types of the hive partitions in a struct:

```sql
SELECT * FROM read_parquet('dir/**/*.parquet', hive_partitioning = true,
    hive_types = {'release': DATE, 'orders': BIGINT});
```
Auto-detected types are `DATE`, `TIMESTAMP` and `BIGINT`; disable that casting with `hive_types_autocast = 0`.

Writing such a layout uses `COPY ... (PARTITION_BY ...)`; see duckdb-partitioned-writes. `PARTITION_BY` takes columns only, not expressions, so compute them in a subquery:

```sql
COPY (SELECT *, year(timestamp) AS year, month(timestamp) AS month FROM services)
TO 'test' (PARTITION_BY (year, month));
```

## Checked

2026-11-07. Read the Hive Partitioning page in full and confirmed the read and COPY examples, the PARTITION_BY no-expressions note and subquery workaround, the year/month layout, the `hive_partitioning` flag, partition filter pushdown example, auto-detection and `SET hive_partitioning = false`, `hive_types` and `hive_types_autocast = 0`. Removed the claim that the parameter exists on read_csv and read_json (the page only shows read_parquet), the statement that partition values are strings, the unsupported pushdown gotcha and the Verify step.

Method: documentation only; no commands were run.
