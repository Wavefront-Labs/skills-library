---
id: computing-software.web-development.hasura.hasura-native-queries-logical-models
name: hasura-native-queries-logical-models
category: computing-software
field: web-development
product: hasura
tags: [hasura, native-queries, logical-models, sql, postgres]
level: advanced
status: docs-checked
description: "Expose parameterized raw SQL as a GraphQL field using Hasura Native Queries backed by a Logical Model, without needing DDL privileges."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/schema/postgres/native-queries.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/schema/postgres/logical-models.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: query custom SQL (GROUP BY, window functions, scalar functions) through GraphQL without creating database objects that need DDL privileges.

Supported from: Cloud and Enterprise v2.26.0, Community v2.28.0.

Concepts:
- A Logical Model describes the returned shape: fields with `type` (a PostgreSQL type or a reference to another Logical Model), `nullable` and optional `description`.
- A Native Query has `root_field_name`, `arguments`, `code` (SQL) and `returns` (the Logical Model name).
- Arguments are used in SQL as `{{arg_name}}`, and may appear more than once. They behave like parameterized-query variables, so need no quoting; they cannot supply structure such as a table name in FROM. For LIKE use `LIKE ('%' || {{searchTitle}} || '%')`.

Metadata (databases.yaml, under the source):

```yaml
logical_models:
  - name: article_excerpt
    fields:
      id:
        type: integer
      excerpt:
        type: text
native_queries:
  - root_field_name: article_with_excerpt
    arguments:
      max_length:
        type: integer
    code: SELECT id, substring(content, 1, {{max_length}}) AS excerpt FROM article
    returns: article_excerpt
```
Metadata API equivalents: `pg_track_logical_model`, `pg_track_native_query` (with `"type": "query"`), `pg_untrack_logical_model`. Console: Data tab, Native Queries in the sidebar (Logical Models tab, Native Queries tab).

Query it with the `args` parameter plus the usual `where`, `order_by`, `distinct_on`, `limit`, `offset`:

```graphql
query { article_with_excerpt(args: { max_length: 20 }, where: { date: { _gte: "2023-03-01" } }) { id excerpt } }
```
Rules:
- SQL must be a single read-only, standalone query, must match the Logical Model, and cannot invoke a stored procedure. Mutations are not supported.
- Hasura aggregations are not supported; write the aggregation in the SQL.
- Live-query subscriptions work; streaming subscriptions do not.
- A Logical Model has no permissions by default, so only admin can use it. Add `select_permissions` (columns list or `"*"`, plus a filter such as `{}`) or `pg_create_logical_model_select_permission`. Native Queries inherit the Logical Model's permissions.
- A Logical Model attached to a Native Query cannot be removed until the Native Query is.
- Models and queries that refer to each other must be tracked together in one `bulk_atomic` call.
- Relationships between Native Queries (and to tables in the same source) are given when tracking the Native Query, via `object_relationships`/`array_relationships` with `column_mapping` and `remote_native_query` or `remote_table`. The page's info box also says relationships will come in a future release, which conflicts with its Relationships sections.

## Checked
2026-11-07. Read in full both cited pages (native-queries.mdx, logical-models.mdx; GitHub file view, no snippet files; Console screenshots are not in the text).
Confirmed: every item above. The yaml example is trimmed from the page's own example.
Removed: the "relationships were noted as a future feature" gotcha as the only word (the page also documents relationships), the invented Verify step. Added the SQL restrictions, permissions, streaming and bulk_atomic notes.
Method: documentation only; no commands were run.
