---
id: computing-software.database-administration.clickhouse.merge-table-function-across-tables
name: merge-table-function-across-tables
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, merge, table-function, table, variant, schema]
level: practitioner
status: docs-checked
description: "Query many similarly named ClickHouse tables with the merge() table function, using _table and Variant functions when column types differ."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/developer/merge-table-function.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# merge table function across tables
The `merge` table function queries multiple tables in parallel by creating a temporary Merge table whose structure is the union of their columns, with common types derived.
```sql
SELECT loser_name, score
FROM merge('atp_matches*')
WHERE winner_name = 'John McEnroe'
AND loser_seed = 1;
```
The docs example has one table per decade (`atp_matches_1960s` ... `atp_matches_1990s`) with slightly different schemas: `winner_seed` is `Nullable(String)`, `Nullable(UInt8)` or `Nullable(UInt16)`, `score` is `String` or `Array(String)`, and only the 1990s table has `walkover` and `retirement` columns.

Where types differ across tables, the merged column can hold several types, so check the type per row with `variantType` and read it with `variantElement`:
```sql
SELECT loser_name, score, winner_seed
FROM merge('atp_matches*')
WHERE winner_name = 'John McEnroe'
AND loser_seed = 1
AND multiIf(
  variantType(winner_seed) = 'UInt8', variantElement(winner_seed, 'UInt8') >= 3,
  variantType(winner_seed) = 'UInt16', variantElement(winner_seed, 'UInt16') >= 3,
  variantElement(winner_seed, 'String')::UInt16 >= 3
);
```
The `_table` virtual column says which source table each row came from, e.g. `SELECT _table, walkover, count() FROM merge('atp_matches*') GROUP BY ALL ORDER BY _table`. A column that exists in only some tables is NULL for the others (`walkover` is NULL except in the 1990s table), so derive it from other columns where needed (the docs search `score` for `W/O`).

## Checked
2026-11-03. Confirmed against the "Merge table function" page. Fixed: the skill said differing types are resolved to a common type that may change values; the page shows differing types handled as Variant (`variantType`/`variantElement`). Removed: the claim that the argument is a regex and the `^atp_matches_` anchoring advice, the `SELECT DISTINCT _table` Verify step, and the long UNION ALL comparison, none of which are on the page.
Method: documentation only; no commands were run.
