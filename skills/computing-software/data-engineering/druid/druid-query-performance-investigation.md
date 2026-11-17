---
id: computing-software.data-engineering.druid.druid-query-performance-investigation
name: druid-query-performance-investigation
category: computing-software
field: data-engineering
product: druid
tags: [explain-plan, query-metrics, sql-tuning, slow-queries, troubleshooting]
level: practitioner
status: docs-checked
description: "Investigate slow SQL with metrics and the explain plan."
sources:
  - https://github.com/apache/druid/blob/master/docs/querying/tips-good-queries.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Query performance depends heavily on how data was ingested, so first follow the schema design best practices.

If queries are slower than expected, two tools are named:
- Query metrics: configure Druid processes to emit metrics for query execution and monitor them.
- Explain plan: shows the full query details and every operation Druid performs. Use it to spot areas to improve. The docs link to a reference for interpreting the output, and to a tutorial on the Query view in the web console.

Start with metrics to see which part of execution is slow, then use the explain plan to see what Druid actually executes.

Settings that help:
- Turn on query caching. The biggest gains are for TopN and timeseries queries; for GroupBy queries whose bottleneck is merging on the Broker, caching helps little.
- Use TopN approximation: a SQL query with GROUP BY on one dimension and ORDER BY on one aggregate lets Druid use TopN by default. TopN is approximate because each data process returns only its top K results to the Broker.

Query tuning:
- Query one table at a time, and select only the columns you need.
- Filter, always on time, and minimize inequality filters because they are very resource-intensive.
- Keep queries short; a UNION ALL over many datasources can be split into per-datasource queries whose results you aggregate yourself.
- Minimize or remove subqueries; consider pre-computing them as a join or part of the datasource.
- Consider Timeseries and TopN instead of GroupBy, and avoid grouping on high-cardinality columns such as user ID; filter first.
- Query smaller time intervals and combine results client-side.
- Reduce transformations, functions and expressions.

## Checked

2026-11-08. Read querying/tips-good-queries.md in full. Added the caching, TopN approximation and manual tuning tips. Did not copy the page's final sample query, which has an empty FLOOR() call and misordered WHERE.

Method: documentation only; no commands were run.
