---
id: computing-software.web-development.hasura.hasura-upsert-on-conflict
name: hasura-upsert-on-conflict
category: computing-software
field: web-development
product: hasura
tags: [hasura, mutations, upsert, on-conflict, constraint, postgres]
level: practitioner
status: docs-checked
description: "Upsert with Hasura insert mutations using on_conflict constraint, update_columns and an optional where, and understand how upsert differs from update."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/mutations/postgres/upsert.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: insert-or-update safely.

Add `on_conflict` to an insert mutation (example from the docs):

```graphql
mutation upsert_article {
  insert_article(
    objects: [{ title: "Article 1", content: "Updated article 1 content", published_on: "2018-10-12" }],
    on_conflict: { constraint: article_title_key, update_columns: [content] }
  ) { returning { id title content published_on } }
}
```
Here `published_on` is left unchanged because it is not in `update_columns`.

Rules from the docs:
- `constraint` names a unique or primary key constraint. Hasura generates enum values for it (try autocomplete in GraphiQL); typically `<table-name>_<column-name>_key`. Partial unique indexes cannot be used.
- `update_columns` lists the columns to update on conflict. An empty array ignores the request on conflict.
- A `where` inside `on_conflict` checks a condition before the update, for example `where: { published_on: {_lt: "2018-10-12"} }`.
- Only tables with update permissions are upsertable; the table's update permissions are respected before updating an existing row.
- Look up constraint names with `SELECT * FROM "information_schema"."table_constraints" WHERE table_name='<table>' AND table_schema='<schema>';`.
- `on_conflict` can also be given on nested objects.

Upsert is not a substitute for update: Postgres first tries to insert, so all columns necessary for an insert are required; otherwise an error like `NULL value unexpected for <not-specified-column>` can occur. If you know the row exists, use an update mutation.

Nested upsert caveat: it fails when the parent upsert (array relationship) or the nested object upsert (object relationship) affects no rows, for example `update_columns: []` and a conflict occurs. The docs say to set `update_columns: [<conflict-columns>]` in that case, which rewrites the conflicting columns with the same values.

## Checked
2026-11-07. Read in full the single cited page (upsert.mdx, GitHub file view; no snippet files, only inline GraphiQL components).
Confirmed: every rule above, the information_schema query, the constraint naming, the not-a-substitute section, the nested caveat.
Removed: the original `article_pkey` / `affected_rows` example (replaced with the page's example), the "forces row to exist" style Verify step, and the "usually" wording that was not tied to the page.
Method: documentation only; no commands were run.
