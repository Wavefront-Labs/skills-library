---
id: computing-software.web-development.hasura.hasura-aggregation-queries
name: hasura-aggregation-queries
category: computing-software
field: web-development
product: hasura
tags: [hasura, queries, aggregate, count, sum, avg, postgres]
level: intro
status: docs-checked
description: "Fetch counts, sums, averages and maxima in Hasura using the <table>_aggregate field and nested array-relationship aggregates."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/queries/postgres/aggregation-queries.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: aggregate data without custom SQL.

The aggregate field name is the table name plus `_aggregate`. It returns an `aggregate` object (`count`, `sum`, `avg`, `max`, `min`, etc.) alongside `nodes`:

```graphql
query {
  articles_aggregate {
    aggregate {
      count
      sum { rating }
      avg { rating }
      max { rating }
    }
    nodes { id title rating }
  }
}
```
Nested aggregation on an array relationship:

```graphql
authors(where: { id: { _eq: 1 } }) {
  id
  name
  articles_aggregate { aggregate { count avg { rating } } }
}
```
Notes:
- Not all aggregate functions exist for every data type.
- For more advanced needs the docs point to views or custom SQL functions.
- Arguments such as `where` can be used on the aggregate field (the nested example filters the parent with `where: { id: { _eq: 1 } }`).

## Checked

2026-11-04. Confirmed against the cited pages: aggregation-queries page: field name suffix, aggregate and nodes examples, nested aggregation, data-type caveat, views/custom functions pointer. Removed or corrected: Native Queries pointer, aggregation-permission and allow_aggregations claims (not on the cited page; see the permissions skill), distinct_on/limit scoping and the Verify step.

Method: documentation only; no commands were run.
