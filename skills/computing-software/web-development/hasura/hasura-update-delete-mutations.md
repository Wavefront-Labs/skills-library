---
id: computing-software.web-development.hasura.hasura-update-delete-mutations
name: hasura-update-delete-mutations
category: computing-software
field: web-development
product: hasura
tags: [hasura, mutations, update, delete, set, inc, primary-key]
level: practitioner
status: docs-checked
description: "Use Hasura update_<table>, update_<table>_by_pk and delete_<table> mutations with where filters and the _set and _inc operators."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/mutations/postgres/update.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/mutations/postgres/delete.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: modify or remove rows precisely.

Update:
```graphql
mutation {
  update_article(where: { id: { _eq: 3 } }, _set: { title: "New" }, _inc: { rating: 1 }) {
    affected_rows
    returning { id title rating }
  }
}
```
- `where` is compulsory; the `{}` expression updates all rows.
- At least one of `_set`, `_inc` or the jsonb operators (`_append`, `_prepend`, `_delete_key`, `_delete_elem`, `_delete_at_path`) is required.
- `update_article_by_pk(pk_columns: {id: 1}, _set: {...})` returns the updated row or null if it does not exist. It is available only with select permission on at least the primary key columns and update permission on at least one column (supported from v1.2.0).
- `update_article_many(updates: [{ where: ..., _set: ... }, ...])` runs several updates in sequence in one transaction (supported from v2.10.0); the result is an array in order.
- `_inc` takes negative values to decrement.

Delete:
```graphql
mutation {
  delete_article(where: { rating: { _lt: 2 } }) { affected_rows }
  delete_article_by_pk(id: 1) { id }
}
```
`where` is compulsory; `{}` deletes all rows. `delete_<table>_by_pk` returns the deleted row (or null) and needs select permission on the table (supported from v1.2.0).

Non-public tables use `update_<schema_name>_<table_name>` and `delete_<schema_name>_<table_name>`.

Gotcha: the docs say nested updates are not supported; to replace a list of nested objects, delete the existing ones and insert the new list in two mutations.

## Checked
2026-11-07. Read in full both cited pages (update.mdx and delete.mdx, GitHub file view; no snippet files, only inline GraphiQL and TOC components).
Confirmed: where compulsory and `{}`, the operator requirement, by_pk behaviour and permissions, version notes, naming for non-public schemas, update_many, `_inc` decrement.
Removed: the "guard it with permissions and filters" advice (not on the pages) and the invented Verify step. The combined `_set` plus `_inc` example is a composition of two documented operators; the pages show them in separate examples.
Method: documentation only; no commands were run.
