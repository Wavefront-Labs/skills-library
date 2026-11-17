---
id: computing-software.data-engineering.data-modelling.modelling-json-and-variant-data
name: modelling-json-and-variant-data
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, semi-structured-data, json-modelling, variant, flatten, nested-structs, schema-on-read, bigquery-json, snowflake-variant, databricks-variant]
level: practitioner
status: docs-checked
description: "Model semi-structured JSON in a warehouse: land raw as VARIANT/JSON, extract typed columns, flatten arrays to child tables, keep nested structs where useful, and handle drift."
sources:
  - https://docs.snowflake.com/en/user-guide/semistructured-considerations
  - https://docs.snowflake.com/en/sql-reference/functions/flatten
  - https://cloud.google.com/bigquery/docs/json-data
  - https://cloud.google.com/bigquery/docs/best-practices-performance-nested
  - https://docs.databricks.com/aws/en/semi-structured/variant
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modelling JSON / VARIANT data

**Goal:** keep the flexibility of raw JSON for ingestion while giving analysts typed, documented, fast columns.

## 1. Layering
| Layer | Shape |
|---|---|
| Raw/bronze | one row per payload: `payload VARIANT/JSON`, ingest metadata. Never reshaped. |
| Staging/silver | typed columns extracted for every field consumers use; arrays exploded into child tables; payload kept for re-extraction |
| Marts | ordinary relational/star models; no JSON paths in BI |

## 2. Extract with explicit types
```sql
-- Snowflake
SELECT payload:order_id::NUMBER AS order_id, payload:customer.email::STRING AS email,
       payload:created_at::TIMESTAMP_TZ AS created_at, payload:amount::NUMBER(18,2) AS amount
FROM raw.orders_json;
-- BigQuery (JSON type)
SELECT LAX_INT64(payload.order_id) AS order_id,
       JSON_VALUE(payload, '$.customer.email') AS email
FROM raw.orders_json;
-- Databricks VARIANT
SELECT payload:order_id::BIGINT, payload:customer.email::STRING, payload:amount::DECIMAL(18,2)
FROM raw.orders_json;
```
- Always cast; untyped extracts return VARIANT/JSON strings that compare and sort wrongly.
- Use `try_variant_get` (Databricks) or the `LAX_` functions (BigQuery) where producers send bad types, and test the null rate.
- Key names are case-sensitive in JSON paths.

## 3. Arrays → child tables
```sql
-- Snowflake: one row per line item
SELECT o.payload:order_id::NUMBER AS order_id, li.index AS line_no,
       li.value:sku::STRING AS sku, li.value:qty::INT AS qty
FROM raw.orders_json o, LATERAL FLATTEN(input => o.payload:items) li;
-- BigQuery: JSON_QUERY_ARRAY(payload, '$.items') returns ARRAY<JSON>; unnest it to get one row per item
-- Databricks: LATERAL VIEW explode / variant_explode(payload:items)
```
- The child table's grain is (parent key, array index or item id) — declare and test it.
- Snowflake `OUTER => TRUE` keeps input rows whose array cannot be expanded; use a left join to the unnested array in BigQuery.

## 4. When to keep nesting
- BigQuery and Databricks/Spark handle `STRUCT`/`ARRAY<STRUCT>` columns efficiently; keeping line items nested in the order row avoids a join and is natural for "order with its items" queries. Explode only for item-level analysis.
- Snowflake VARIANT: see the semi-structured considerations page for how storage and query performance behave; types are only as good as the data.
- Wide sparse attributes (hundreds of optional keys, e.g. product attributes) → keep as VARIANT/MAP in silver and extract only the used ones.

## 5. Schema drift
- Profile keys regularly (`FLATTEN(... RECURSIVE => TRUE)` → distinct paths and types) and diff against the extraction list.
- Alert on new keys and type changes; add columns deliberately.
- Keep raw payload so new fields can be backfilled by re-running staging.

## Verify
- [ ] No mart or dashboard query uses JSON path syntax.
- [ ] Child tables have tested unique keys (parent id + index/item id).
- [ ] Null rate of each extracted column monitored (sudden 100% null = renamed key).

## Checked

2026-10-28. Confirmed: Snowflake FLATTEN arguments `OUTER` and `RECURSIVE`; BigQuery `JSON_QUERY_ARRAY` returns ARRAY<JSON>, `JSON_VALUE` and `LAX_INT64`; Databricks `variant_explode`, `try_variant_get` and `:` path syntax. Removed: BigQuery `INT64()`/`STRING()` extraction, `TRY_CAST`/`SAFE_CAST`, `WITH OFFSET`, Databricks `try_cast` on VARIANT, the Snowflake columnar-storage claim (not found in the fetched pages).

Method: documentation only; no commands were run.
