---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.sql-plugin-queries
name: sql-plugin-queries
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, sql-plugin-queries]
level: practitioner
status: docs-checked
description: "Query OpenSearch with SQL via _plugins/_sql: jdbc, csv and raw formats, fetch_size cursor paging, _explain, and the documented limits on joins and subqueries."
sources:
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_sql-and-ppl/sql-and-ppl-api/index.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_sql-and-ppl/sql/basic.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_sql-and-ppl/response-formats.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_sql-and-ppl/limitation.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_sql-and-ppl/settings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSearch SQL queries

**Goal:** SQL access to OpenSearch indexes for analysts, using the SQL plugin. (Elasticsearch has its own, separate SQL feature; this skill covers the OpenSearch plugin only.)

## Run a query
- `POST _plugins/_sql {"query":"SELECT host, COUNT(*) FROM logs-* WHERE status >= 500 GROUP BY host"}`.
- Supported clauses: `SELECT [DISTINCT]`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT [offset,] size`. Only `SELECT` and `FROM` are required. An index pattern such as `FROM account*` is allowed.
- `LIMIT 1, 1` maps to `from` and `size`; fine for small indexes, inefficient on large ones. Use `ORDER BY` so pages stay in the same order.
- `IS NULL` does not distinguish a missing field from one explicitly set to null. In `ORDER BY`, nulls and missing values go last by default.

## Response formats
- Query parameter `format`: `jdbc` (default, includes `schema`, `datarows`, `total`, `size`, `status`), `csv`, `raw` (pipe-delimited).
- `sanitize` (default `true`): in CSV, cells starting with `+`, `-`, `=` or `@` get a leading single quote and cells containing commas are double-quoted; in `raw`, cells containing `|` are double-quoted. Keep it on for data that opens in a spreadsheet (formula injection).

## Paging
- `"fetch_size": 500` in the body returns a `cursor`; send `{"cursor": "..."}` to `_plugins/_sql` for the next page. Default `fetch_size` is 1,000; `0` means no paging. The last page has no cursor.
- Close early with `POST _plugins/_sql/close {"cursor":"..."}` (response `{"succeeded":true}`).
- `fetch_size` needs the `jdbc` format and only works for basic queries: aggregation and join queries do not support it. `plugins.sql.cursor.keep_alive` (default `1m`) is how long the cursor context stays open.

## Inspect and filter
- `POST _plugins/_sql/_explain` returns the generated DSL (or a plan for queries that need post-processing).
- A `filter` body field adds a DSL filter to the query; `parameters` supplies values for `?` placeholders in prepared queries.

## Limits to design around
- Aggregation functions take fields only, not expressions (`avg(log(age))` is not supported).
- A `FROM` subquery works only when it can be merged into one query; not if the outer query has `GROUP BY` or `ORDER BY`.
- `JOIN` is best effort: no aggregation on the joined result, and the documentation warns of performance problems above 5 million matching records. Joins stop after 60 seconds by default; the `/*! JOIN_TIME_OUT(seconds) */` hint changes it. Filter both sides by key range first.
- The limitations page says `DELETE` is not supported: use the Delete by Query API instead.
- Result rows are capped by `plugins.query.size_limit` (default `10000`). `plugins.sql.enabled` (default `true`) switches the SQL endpoint off. Setting `rest.action.multi.allow_explicit_index` to `false` disables both the SQL and PPL endpoints.
- Engine differences: since 3.0.0 an experimental Calcite engine exists (`plugins.calcite.enabled`); the settings page lists it as default `true`, so check what your version does with joins and subqueries.

## Verify
- [ ] The DSL from `_explain` returns the same count as the SQL result.
- [ ] A paged query returns a `cursor` until the last page, then none.

## Checked
2026-11-08. Confirmed against the OpenSearch documentation source pages for the SQL and PPL API, basic queries, response formats, limitations and settings: clauses, formats and sanitize rules, `fetch_size` default and jdbc-only rule, cursor close endpoint, explain endpoint, `filter` and `parameters`, join timeout and hint, 5 million record warning, `size_limit`, `cursor.keep_alive`, `plugins.sql.enabled`. Removed: the claim that dashed index names need backticks (not stated on any page read), the claim about Elasticsearch SQL parity, and the generic notes.
Method: documentation only; no commands were run.
