---
id: computing-software.web-development.hasura.hasura-keyset-pagination-and-total-count
name: hasura-keyset-pagination-and-total-count
category: computing-software
field: web-development
product: hasura
tags: [hasura, queries, pagination, keyset, cursor, aggregate, subscriptions]
level: practitioner
status: docs-checked
description: "Page Hasura results with a unique sequential cursor column in where instead of offset, and return a total count alongside a limited page."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/queries/postgres/pagination.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: fast, duplicate-free pagination.

Keyset (cursor) pagination replaces offset with a where filter on a unique, sequential column:

```graphql
query {
  authors(where: { id: { _gt: 5 } }, order_by: { id: asc }, limit: 5) { id name }
}
```
Offset paging is `limit: 5, offset: 5` (offset is also allowed on nested relationships). Rules for keyset paging from the docs:
- The cursor column(s) must be unique and sequential. Commonly an auto-incrementing id (integer or big integer) or `created_at` when no order is explicit.
- If the query has `order_by`, the `order_by` column(s) need to be used as the cursor.
- Keyset paging reads after a specific row rather than by position, so no duplicates, and it is more performant than offset because it can use database indexes on the cursor columns.

Total count with a page, in one request:

```graphql
query {
  articles_aggregate(where: { rating: { _gt: 3 } }) { aggregate { count } }
  articles(where: { rating: { _gt: 3 } }, limit: 10) { id title }
}
```
Use the count and limit to compute number of pages.

Gotcha: over subscriptions you cannot do this in one operation because a GraphQL subscription may only have one root field; run two subscriptions.

## Checked

2026-11-04. Confirmed against the cited pages: pagination page: limit/offset, nested limits, keyset rules and performance note, aggregate-count example, single-root-field subscription caveat. Removed or corrected: the Verify step.

Method: documentation only; no commands were run.
