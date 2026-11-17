---
id: computing-software.database-administration.clickhouse.json-column-type-usage
name: json-column-type-usage
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, json, dynamic-paths, type-hints, skip, max-dynamic-paths]
level: practitioner
status: docs-checked
description: "Use ClickHouse's JSON column type only for dynamic structures, with type hints, SKIP paths and a bounded max_dynamic_paths."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/json_type.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# json column type usage
JSON is a column type, not a data format: you can insert JSON text into ordinary columns via `JSONEachRow` without using it. Use the JSON type only when the structure is dynamic. If the schema is static, even when the data arrives as NDJSON or contains nested structures, define classic types (the docs model a predictable arXiv document with `Array(Tuple(created String, version String))` and `Array(Array(String))` columns instead).

Tips from the page:
- Give type hints for known paths in the column definition. Hinted paths are stored like traditional columns with no discriminator columns or dynamic resolution at query time, so they perform as top-level fields would.
- Use `SKIP` and `SKIP REGEXP` for paths you do not need, to reduce storage and improve performance.
- Keep `max_dynamic_paths` low; as a rule of thumb below 10,000, since large values increase resource consumption.
- JSON columns can be in the primary key like other columns; codecs cannot be specified for a subcolumn. Query syntax may need special casting or operators for nested fields; read nested sub-objects with `.^`.

Docs examples. A hint for a column used in the ordering key (it tells ClickHouse the column is not null and which `update_date` subcolumn to use):
```sql
CREATE TABLE arxiv
(
  `doc` JSON(update_date Date)
)
ENGINE = MergeTree
ORDER BY doc.update_date
```
The docs generally prefer keeping the stable columns typed and adding a JSON column only for the dynamic part, e.g. `tags JSON()`, which minimises inference. Introspect the inferred paths and types with `JSONAllPathsWithTypes()` and `JSONDynamicPaths()`:
```sql
SELECT JSONAllPathsWithTypes(tags)
FROM arxiv
FORMAT PrettyJSONEachRow
```

## Checked
2026-11-03. Confirmed against the "Use JSON where appropriate" page. Removed: the invented `JSON(max_dynamic_paths=256, user_id UInt64, SKIP debug)` example (the page shows no SKIP syntax inside a definition), the `logs` table, and the "test casts" gotcha.
Method: documentation only; no commands were run.
