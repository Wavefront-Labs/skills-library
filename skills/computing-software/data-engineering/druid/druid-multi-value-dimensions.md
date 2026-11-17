---
id: computing-software.data-engineering.druid.druid-multi-value-dimensions
name: druid-multi-value-dimensions
category: computing-software
field: data-engineering
product: druid
tags: [multi-value-dimensions, arrays, tags, group-by, filtering]
level: practitioner
status: docs-checked
description: "Ingest, filter and group Druid multi-value string dimensions, and tell them apart from SQL array columns."
sources:
  - https://github.com/apache/druid/blob/master/docs/querying/multi-value-dimensions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Multi-value string dimensions come from input fields holding an array of values, such as `"tags": ["t1","t2","t3"]`. They are distinct from array types: arrays act like standard SQL arrays, multi-value dimensions do not. The docs recommend arrays whenever possible (newer, SQL-compliant).

## Ingestion

- Native batch and streaming: the console data loader can detect them. CSV/TSV use `listDelimiter` in the `inputFormat`; JSON must be a real JSON array. Dimension entry: type `string`, `multiValueHandling` and optionally `createBitmapIndex`.
- `multiValueHandling`: `SORTED_ARRAY` (default; sorts values), `SORTED_SET` (sorts and removes duplicates), `ARRAY` (keeps original order).
- SQL-based ingestion (MSQ): `multiValueHandling` is not available. Use `ARRAY_TO_MV(array)` to turn a `VARCHAR ARRAY` into a multi-value `VARCHAR`, and `MV_TO_ARRAY` for the reverse. For rollup, group on the array form and convert after grouping: `GROUP BY ..., "tags"` with `ARRAY_TO_MV("tags")` in the SELECT. If the column is declared `VARCHAR` in `EXTERN`, use `GROUP BY MV_TO_ARRAY("tags")` and `ARRAY_TO_MV(MV_TO_ARRAY("tags"))` in the SELECT, since MSQ groups multi-value dimensions only as arrays.

## Filtering

- Value filters (selector, bound, in) match a row if any one value matches. The column comparison filter matches if the dimensions overlap.
- Filters matching `null` or `""` match empty cells; an empty multi-value row counts as `null`.
- Logical `and`, `or`, `not` behave as on single-value dimensions. Native queries can express an `and` of two selectors on the same multi-value dimension (matching a row with both values), which SQL treats as a contradiction.

## Grouping

Grouping (SQL, topN, groupBy) produces one group per value across all matching rows, like an implicit `UNNEST`, so there can be more groups than rows. The filter applies to the row before explosion: filtering `tags = 't3'` still returns groups for the other tags on those rows.
- To keep only matching values use SQL `MV_FILTER_ONLY` / `MV_FILTER_NONE`, a filtered virtual column, or a filtered dimensionSpec (for example `listFiltered` with `values`). A filtered dimensionSpec is much more efficient than a `having` spec, since it applies at the lowest level of processing.
- Safety switch: query context `groupByEnableMultiValueUnnesting: false` makes groupBy return an error instead of unnesting, to catch unexpected multi-value columns.

## Arrays vs multi-value dimensions

They are stored as different column types with different query behaviour. Convert with `MV_TO_ARRAY` and `ARRAY_TO_MV`.
- Get arrays: JSON specs with dimension type `auto` or `useSchemaDiscovery` enabled; in SQL ingestion, a query that generates arrays. Arrays can hold strings or numbers.
- Get multi-value dimensions: JSON specs with type `string` and no schema discovery; in SQL ingestion wrap arrays in `ARRAY_TO_MV`. They hold strings only.
- Check which you have: `SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '<table>'`. Arrays show `ARRAY`; multi-value strings show `VARCHAR`.

## Checked

2026-11-08. Read the cited multi-value-dimensions page in full. Rewrote the draft with ingestion options, filter and grouping semantics and the array comparison; removed a claim about MSQ known issues taken from a page not cited here (the cited page itself states `multiValueHandling` is unavailable in MSQ ingestion).

Method: documentation only; no commands were run.
