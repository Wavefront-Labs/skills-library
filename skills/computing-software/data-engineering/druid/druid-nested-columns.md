---
id: computing-software.data-engineering.druid.druid-nested-columns
name: druid-nested-columns
category: computing-software
field: data-engineering
product: druid
tags: [nested-columns, complex-json, json-functions, flatten-spec, transform-spec]
level: practitioner
status: docs-checked
description: "Ingest and query nested JSON in Druid COMPLEX<json> columns with JSON_VALUE, JSON_QUERY and related functions, plus known issues."
sources:
  - https://github.com/apache/druid/blob/master/docs/querying/nested-columns.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Druid stores nested structures in `COMPLEX<json>` columns: a copy of the data as JSON plus specialised internal columns and indexes for nested STRING, LONG, DOUBLE values and arrays of those. An optimised virtual column reads and filters them at speeds close to ordinary columns. Ingestion is automatically type-optimised: only LONG values store as a LONG column, arrays as ARRAY columns, otherwise `COMPLEX<json>` (the same mechanism as type-aware schema discovery). Source formats: JSON, Parquet, Avro, ORC, Protobuf.

## Ingestion

- Native batch or streaming (for example a Kafka supervisor): in `dimensionsSpec.dimensions` list the nested field as `{"type": "json", "name": "<field>"}`.
- SQL-based ingestion: declare the column type as `COMPLEX<json>` in the `EXTERN` row signature.
- Flattening alternative: JSON functions in a `transformSpec` (native) or the SELECT of INSERT/REPLACE (SQL) can replace a `flattenSpec`. For example native transforms like `json_value(shipTo, '$.firstName')`, `json_query(shipTo, '$.address')`, `json_object('product', product, ...)`.
- Serialized JSON strings: use `parse_json` in a `transformSpec` transform, or `PARSE_JSON` in SQL. Use `try_parse_json` / `TRY_PARSE_JSON` if values may be invalid; invalid values become null. Text formats like `tsv` require this route to fill a `COMPLEX<json>` column.

## Querying

- Druid supports a small subset of JSONPath, mainly for extracting single values (see the SQL JSON functions reference).
- `SELECT *` on a nested column returns the JSON object, so you cannot group, aggregate or filter on it directly.
- `JSON_VALUE(col, '$.path')` is optimised to read the nested columns and indexes and is the recommended function for performance. Numeric filters can use indexes not available on plain LONG/DOUBLE columns. It returns only primitives (`STRING`, `LONG`, `DOUBLE`, and with `RETURNING` also `ARRAY<STRING|LONG|DOUBLE>`); a path pointing at an object or array (without an array `RETURNING` type) returns null. Default type is VARCHAR; add `RETURNING BIGINT`, `DECIMAL` or `VARCHAR` as a type hint. A shorthand like `shipTo:address.country` also works.
- `JSON_VALUE` can be used in `WHERE`, `GROUP BY` and aggregates like ordinary columns.
- Transform functions: `JSON_QUERY` (extracts objects and arrays, unlike `JSON_VALUE`), `JSON_OBJECT(KEY 'k' VALUE ...)`, `PARSE_JSON`, `TO_JSON_STRING`. Helpers for inspecting structure: `JSON_KEYS` and `JSON_PATHS`.
- Check types with `INFORMATION_SCHEMA.COLUMNS`; nested columns show `COMPLEX<json>`.

## Known issues

- Using `COMPLEX<json>` directly in grouping, filtering or aggregator inputs is not well integrated and may error or behave undefined; workaround: coerce with `TO_JSON_STRING` first.
- Array outputs of `JSON_KEYS` / `JSON_PATHS` can be grouped and used with array functions such as `ARRAY_CONCAT_AGG`, but filtering with `=` or `IS NULL` is not well defined.
- Input validation of the JSON SQL operators is incomplete, giving undefined behaviour or unhelpful errors.
- Very complex nested structures are expensive to ingest; treat each nested primitive as a flattened top-level column when tuning memory and task runtime.

## Checked

2026-11-08. Read the cited nested-columns page in full. Expanded the draft with ingestion routes, `JSON_VALUE` semantics, transform and helper functions, and the known issues list.

Method: documentation only; no commands were run.
