---
id: computing-software.data-engineering.druid.druid-query-context-settings
name: druid-query-context-settings
category: computing-software
field: data-engineering
product: druid
tags: [query-context, timeout, priority, sql-query-context, time-zone]
level: practitioner
status: docs-checked
description: "Set query context for timeouts, priority and SQL behaviour."
sources:
  - https://github.com/apache/druid/blob/master/docs/querying/query-context.md
  - https://github.com/apache/druid/blob/master/docs/querying/sql-query-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The query context controls how an individual query runs. Common uses: override default timeouts for long queries, disable caching while debugging performance, set SQL behaviours such as time zone, set priorities so critical queries get resources first, and adjust memory limits for large datasets.

How you set it depends on the interface and on whether the query is SQL or native. In the web console you can set context parameters for both SQL and native queries from the Query view. Via the API the context is part of the request.

SQL-specific parameters exist in addition to those that apply to all query types. For example `sqlQueryId` sets the SQL query id, which Druid returns in the `X-Druid-SQL-Query-Id` header; use `sqlQueryId` not `queryId`, because setting `queryId` on a SQL request has no effect. Native queries underneath SQL get an auto-generated `queryId`.

## Checked

2026-11-09: confirmed against the Druid Set query context page and the SQL query context page (docs/querying/query-context.md and docs/querying/sql-query-context.md): the listed use cases, that the web console sets context for SQL and native queries, the `context` object in the HTTP API, and the `sqlQueryId` row (returned in the `X-Druid-SQL-Query-Id` header; `queryId` has no effect on SQL requests; underlying native queries get an auto-generated id).

Method: documentation only; no commands were run.
