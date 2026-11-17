---
id: computing-software.data-engineering.etl-pipeline-design.migration-reconciliation-counts-and-checksums
name: migration-reconciliation-counts-and-checksums
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, data-migration, reconciliation, checksums, row-counts, aggregate-validation, cross-platform-hashing, data-validation-tool]
level: practitioner
status: gated
description: "Prove migrated data matches the source: layered checks from row counts to per-column aggregates to row hashes, cross-engine hashing pitfalls, and Google's DVT."
sources:
  - https://github.com/GoogleCloudPlatform/professional-services-data-validator
  - https://docs.snowflake.com/en/sql-reference/functions/hash_agg
  - https://cloud.google.com/bigquery/docs/reference/standard-sql/hash_functions
  - https://github.com/erezsh/reladiff
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migration reconciliation: counts and checksums

**Goal:** objective evidence that every migrated table is complete and identical, cheap enough to rerun daily during a parallel run.

Run here on DuckDB 1.5.6: the partition aggregate query and the row-hash query executed (with `strftime(updated_at, '%Y-%m-%d %H:%M:%S.%f')` in place of `TO_CHAR`, which is Oracle/Snowflake syntax). Observed: `||` and `concat` behave differently on NULL across engines (DuckDB `concat('a',NULL,'b')` gave `ab`, `'a'||NULL||'b'` gave NULL, and `CONCAT_WS('|','a',NULL,'b')` gave `a|b` by skipping NULL), so keep the `COALESCE(..., '<NULL>')` wrapper to preserve column positions. Cross-engine hash equality, Snowflake `HASH_AGG`, the Data Validation Tool CLI and reladiff were not run (gated: unconfirmed, source is paywalled or blocked).

## 1. Layer the checks (cheap → expensive)
1. **Schema**: column names, types, nullability mapped as planned.
2. **Row count** per table and per partition (date).
3. **Aggregates** per partition: `SUM` of numerics, `COUNT(DISTINCT key)`, `MIN/MAX` of dates, `COUNT(col)` (non-null count) per column.
4. **Row hash** of all columns for full equality, compared per partition then drilled down.
Stop at the first layer that fails and drill in only there.

## 2. Partition-level aggregate query (run on both sides)
```sql
SELECT order_date,
       COUNT(*)                          AS n,
       COUNT(DISTINCT order_id)          AS n_keys,
       SUM(CAST(amount AS DECIMAL(38,2))) AS sum_amount,
       COUNT(customer_id)                AS nn_customer,
       MIN(updated_at) AS min_upd, MAX(updated_at) AS max_upd
FROM orders GROUP BY order_date;
```
Land both results in one place (the target warehouse) and `FULL OUTER JOIN` on `order_date` to list mismatching days.

## 3. Cross-engine row hashing — normalise first
Hash functions and default string formats differ between engines; hash a canonical string:
- Cast every column to string explicitly: decimals with fixed scale, timestamps as ISO-8601 UTC (`YYYY-MM-DD HH:MI:SS.FFFFFF`), booleans as `0/1`.
- `COALESCE(col, '<NULL>')` — concatenating NULL nulls the whole string in most engines.
- Trim CHAR padding (Teradata/Oracle `CHAR(n)` vs VARCHAR targets); normalise case only if collation was case-insensitive.
- Use a delimiter that cannot appear in data (`'|'` plus escaping, or `\x1f`).
- Use the same algorithm both sides (`MD5`/`SHA256` exist nearly everywhere). Snowflake `HASH_AGG` is fast but Snowflake-only — fine for target-vs-target, not cross-engine.
```sql
-- run on each side, land both outputs in the target, then FULL OUTER JOIN on order_id
SELECT order_id,
       MD5(CONCAT_WS('|',
           COALESCE(CAST(order_id AS VARCHAR), '<NULL>'),
           COALESCE(CAST(CAST(amount AS DECIMAL(18,2)) AS VARCHAR), '<NULL>'),
           COALESCE(TO_CHAR(updated_at, 'YYYY-MM-DD HH24:MI:SS.FF6'), '<NULL>'))) AS row_md5
FROM orders;
```
Function names vary (`TO_CHAR` vs `FORMAT_TIMESTAMP`, `CONCAT_WS` availability); keep one template per engine and test it on a handful of known rows before running at scale.

## 4. Tooling
- **Data Validation Tool (DVT)** — open-source from Google; supports column, row-hash and schema validation across BigQuery, Snowflake, Teradata, Oracle, SQL Server, Postgres, Redshift and others:
```bash
data-validation validate column -sc src_conn -tc bq_conn -tbls db.orders=proj.ds.orders --sum amount --count order_id
data-validation validate row -sc src_conn -tc bq_conn -tbls db.orders=proj.ds.orders --primary-keys order_id --hash '*'
```
- reladiff for key-range checksum bisection between two databases.

## 5. Known benign differences
Float aggregation order (compare rounded), timestamp precision (ms vs µs), timezone conversion on load, trailing spaces, empty string vs NULL (Oracle treats '' as NULL). Document each accepted difference with the rule that normalises it.

## Verify
- [ ] Every table has a reconciliation row: counts, aggregates, hash result, date run.
- [ ] Mismatches are either fixed or recorded as an accepted, normalised difference.
- [ ] Checks run automatically each day of the parallel run.
