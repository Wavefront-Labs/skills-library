---
id: computing-software.web-development.hasura.hasura-sort-and-offset-pagination
name: hasura-sort-and-offset-pagination
category: computing-software
field: web-development
product: hasura
tags: [hasura, queries, order-by, pagination, limit, offset]
level: intro
status: docs-checked
description: "Sort results with order_by (asc, desc, nulls ordering) and page with limit and offset in Hasura queries, including nested lists."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/queries/postgres/sorting.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/queries/postgres/pagination.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: ordered, paged results.

Sorting:
- `order_by` takes an array of objects to sort by multiple columns: `articles(order_by: [{ rating: desc }, { title: asc }])`. Key order inside one object is not preserved, so use a single key per object.
- Sort direction is the `asc` or `desc` enum value for the column. The docs also show `asc_nulls_first`, `asc_nulls_last` and `desc_nulls_last`.
- Default null placement: with ascending order nulls come at the end; with descending order nulls come at the start.
- Nested arrays can be sorted: `authors(order_by: {name: asc}) { articles(order_by: {rating: desc}) { id } }`.
- Sorting by related data: only columns from object relationships and aggregates from array relationships can be used, for example `order_by: { articles_aggregate: { count: desc } }`.
- Scalar computed fields (and aggregates of table computed fields) can be sorted on, from v2.0.2; only for functions with no input arguments other than the table row and Hasura session arguments.

Pagination:
```graphql
authors(limit: 5, offset: 5) { id name }
```
`limit` is the number of rows to retain; `offset` determines which slice to retain. Both also work on nested relationships, such as `articles(limit: 2, offset: 0)`.

Gotcha: offset relies on the position of the row in the dataset. Keyset cursor pagination (a unique, sequential column in a `where`, for example `where: { id: {_gt: 5} }`) avoids duplicates and, per the docs, is more performant because database indexes can be used. If the query has an `order_by`, use those column(s) as the cursor.

## Checked
2026-11-07. Read in full both cited pages (sorting.mdx and pagination.mdx; GitHub file view, no snippet files, only inline GraphiQL and TOC components).
Confirmed: every bullet above.
Removed: `desc_nulls_first` from the enum list (the pages show only the other three), the claim "a stable order_by is needed / large offsets get slow" (not stated; replaced with what the page says about keyset cursors), and the invented Verify step.
Method: documentation only; no commands were run.
