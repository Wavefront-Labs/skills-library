---
id: computing-software.web-development.hasura.hasura-where-filters-and-boolean-logic
name: hasura-where-filters-and-boolean-logic
category: computing-software
field: web-development
product: hasura
tags: [hasura, queries, filters, where, boolean-operators, postgres]
level: intro
status: docs-checked
description: "Filter Hasura query results with the where argument, comparison operators, and _and, _or, _not, including filters across nested relationships."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/queries/postgres/filters/index.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/queries/postgres/filters/comparison-operators.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/queries/postgres/filters/boolean-operators.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write correct where clauses.

Basics:
```graphql
query {
  authors(where: { name: { _eq: "Sidney" } }) { id name }
}
```
- `_eq` and `_neq` work with any Postgres type other than json and jsonb; `_gt`, `_lt`, `_gte`, `_lte` likewise. `_in` and `_nin` take a list; `_is_null` checks for null.
- `_eq` and `_neq` do not return rows with null values; to include them combine with `_is_null` using `_or`.
- Multiple conditions: `_and` and `_or` take arrays of expressions; `_not` inverts a condition. `_or`, `_and` and `_not` combine into arbitrarily complex expressions. If `_or` is given an object instead of an array it behaves like `_and`.

```graphql
articles(where: { _and: [
  { published_on: { _gte: "2017-01-01" } },
  { published_on: { _lte: "2017-12-31" } }
] }) { id title }
```
- Filter by a nested object's fields and filter the nested objects as well:
  `authors(where: { articles: { rating: { _gt: 4 } } }) { id name articles(where: { rating: { _gt: 4 } }) { id title rating } }`.
- Array relationships expose a `where` argument; object relationships have only one nested object and do not.
- `_cast` casts a field before filtering; only jsonb to String and PostGIS geometry to and from geography are supported.
- `where: {}` is the TRUE expression and returns all objects.
- In v2.0.0 and above a null value in a comparison expression (`{ _eq: null }`) throws a type mismatch error.

## Checked
2026-11-07. Read in full all three cited pages (filters index.mdx, comparison-operators.mdx, boolean-operators.mdx; GitHub file view, no snippet files, only inline GraphiQL components).
Confirmed: every bullet above against these pages.
Removed: the "top-level where restricts which authors return, not which articles" gotcha (reworded to what the page shows) and the invented Verify step (compare counts against SQL).
Method: documentation only; no commands were run.
