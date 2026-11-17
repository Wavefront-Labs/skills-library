---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.ppl-queries
name: ppl-queries
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, ppl-queries, os-ppl-sql]
level: practitioner
status: docs-checked
description: "Explore log data with OpenSearch PPL pipes (where, stats, sort, head) via _plugins/_ppl, with explain modes and the query size and timeout settings."
sources:
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_sql-and-ppl/ppl/index.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_sql-and-ppl/ppl/commands/where.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_sql-and-ppl/ppl/commands/stats.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_sql-and-ppl/ppl/commands/sort.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_sql-and-ppl/ppl/commands/head.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_sql-and-ppl/ppl/commands/explain.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_sql-and-ppl/sql-and-ppl-api/index.md
  - https://raw.githubusercontent.com/opensearch-project/documentation-website/main/_sql-and-ppl/settings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Piped Processing Language (PPL) queries

**Goal:** step-by-step, pipe-style exploration of logs and other observability data in OpenSearch. PPL needs the SQL plugin; a minimal distribution may need it installed first.

## Run a query
- `POST _plugins/_ppl {"query":"source=logs-* | where status >= 500 | stats count() as c by host | sort - c | head 10"}`.
- General shape: `search source=<index> | <command> | <command> ...`.
- `where <boolean-expression>` keeps rows where the condition is true. `stats [bucket_nullable=bool] <aggregation>... [by <fields or span(field, interval)>]`: with no `by`, one row for the whole result. Time units for `span` include `ms`, `s`, `m`, `h`, `d`, `w`, `M`, `q`, `y`.
- `sort` has two notations, and one command must stick to one: prefix `sort [count] [+|-] field` (`-` is descending) or suffix `sort [count] field [asc|desc]`. Ascending lists nulls first. Wrap a field in `str()`, `num()`, `ip()` or `auto()` to control how values compare.
- `head [size] [from offset]`: default size 10, default offset 0. The docs say `head` is not rewritten to DSL and runs only on the coordinating node.
- Other commands with their own pages include `fields`, `eval`, `dedup`, `rename` and `parse`; the command list varies with the version.

## See what it does
- `POST _plugins/_ppl/_explain` returns the generated DSL; a query needing post-processing also shows a plan. The `explain` command inside PPL takes modes `simple`, `cost` and `extended` (for example `explain cost source=...`).
- With `plugins.calcite.enabled` true the explain output shows logical and physical plans and a `PushDownContext` listing what was pushed to OpenSearch; with it false, push-down information comes from the v2 engine.

## Limits and settings
- `plugins.query.size_limit` (default `10000`) caps rows returned; `plugins.ppl.query.timeout` (default `5m`) stops long queries; `plugins.ppl.enabled` (default `true`) disables PPL.
- Subsearch, `join` and `lookup` need the Calcite engine (`plugins.calcite.enabled`; the settings page lists the default as `true`, older versions had it off).
- The `format` parameter accepts `jdbc` (default), `csv` or `raw`; `fetch_size` paging is for SQL.

## Verify
- [ ] The explain output shows the filter and aggregation pushed into the request, and the count matches an equivalent DSL aggregation.

## Checked
2026-11-08. Confirmed from the OpenSearch documentation source pages for PPL, the where, stats, sort, head and explain commands, the SQL and PPL API and the settings: syntax, sort notations and null ordering, head defaults and coordinating-node note, span units, explain modes and endpoint, `size_limit`, `ppl.query.timeout`, Calcite-dependent features. Corrected: the earlier `sort - count()` example now sorts on an alias. Removed: the unsupported statement that some functions cannot be pushed down (the pages show push-down only per query) and the generic notes.
Method: documentation only; no commands were run.
