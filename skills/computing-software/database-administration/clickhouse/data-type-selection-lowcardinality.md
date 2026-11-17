---
id: computing-software.database-administration.clickhouse.data-type-selection-lowcardinality
name: data-type-selection-lowcardinality
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, data-types, lowcardinality, nullable, enum]
level: practitioner
status: docs-checked
description: "Select compact ClickHouse data types (narrow numerics, Date over DateTime64, LowCardinality, Enum) and avoid Nullable where possible."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/select_data_type.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# data type selection lowcardinality
Compression efficiency depends mainly on the ordering key, data types and codecs. Guidance from the "Selecting data types" page:
- **Strict types**: use numeric and date types rather than String, for correct filtering and aggregation semantics.
- **Avoid Nullable**: it adds overhead by maintaining separate columns for nulls. Use it only to distinguish empty from null; otherwise default or zero-equivalent values usually suffice.
- **Minimise numeric precision**: pick the narrowest type that fits, e.g. `UInt16` over `Int32` when no negatives are needed and the range fits 0-65535.
- **Date and time**: use `Date` or `Date32` for date-only fields, and `DateTime` over `DateTime64` unless millisecond or finer precision is essential.
- **LowCardinality**: for columns with fewer than approximately 10,000 unique values it reduces storage through dictionary encoding. Use `FixedString` only for strictly fixed-length strings (e.g. country or currency codes).
- **Enum**: 8 or 16 bits depending on the number of values; undeclared values are rejected at insert, and queries can use the natural ordering of values.

Start from schema inference, then tighten:
```sql
DESCRIBE TABLE s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/stackoverflow/parquet/posts/*.parquet')
SETTINGS describe_compact_output = 1
```
By default ClickHouse maps inferred types to `Nullable` because the schema is based on a sample of rows only. To find each column's range and distinct count, the docs suggest `SELECT * APPLY min, * APPLY max, * APPLY uniq FROM table FORMAT Vertical` over a smaller subset, as it can be expensive. In the docs' optimised posts schema: `PostTypeId` becomes an `Enum`, `CreationDate` becomes `DateTime`, `AnswerCount` `UInt16`, `CommentCount` `UInt8`, and `ContentLicense` (3 unique values) `LowCardinality(String)`, which the docs say outperforms `FixedString`.

## Checked
2026-11-03. Confirmed against the "Selecting data types" page. Removed: the mutation-on-type-change and "LowCardinality over millions of values is slower" gotchas, and the `system.parts_columns` Verify query, none of which are on the page.
Method: documentation only; no commands were run.
