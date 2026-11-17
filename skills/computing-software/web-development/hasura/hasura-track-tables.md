---
id: computing-software.web-development.hasura.hasura-track-tables
name: hasura-track-tables
category: computing-software
field: web-development
product: hasura
tags: [hasura, postgres, tables, tracking, metadata, schema]
level: intro
status: docs-checked
description: "Expose Postgres tables over GraphQL by tracking them in Hasura via the Console, tables.yaml metadata, or the API, and create tables through migrations."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/schema/postgres/tables.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make a table appear in the GraphQL API.

Tables can exist in Postgres without being exposed over the GraphQL API; to expose one it must be tracked.

Options:
1. Console: a table created in the Console is tracked by default; for existing tables use the Data -> Schema page.
2. CLI: edit tables.yaml in the metadata directory and apply:

```yaml
- table:
    schema: public
    name: authors
- table:
    schema: public
    name: articles
```
```bash
hasura metadata apply
```
3. API: the `pg_track_table` Metadata API on /v1/metadata, with args `source`, `schema` and `name`.

Creating the table itself:
- add `CREATE TABLE ...` to a manually created migration `up.sql` and `DROP TABLE ...` to `down.sql`, then run `hasura migrate apply`;
- or call the `run_sql` schema API on /v2/query (the docs example sends the `X-Hasura-Role: admin` header).

Once a table is created and tracked, Hasura generates the object type and the query field (`where`, `limit`, `offset`, `order_by`) plus `insert_<table>`, `update_<table>` and `delete_<table>` mutation fields. Comments on tables and columns become GraphQL descriptions.

## Checked
2026-11-07. Read in full the single cited page (tables.mdx, GitHub file view; no snippet files, only inline GraphiQL, Tabs and Thumbnail components).
Confirmed: tracking behaviour, Console default tracking, the tables.yaml block, `hasura metadata apply`, `pg_track_table` args, migration and `run_sql` creation, the generated fields and comment descriptions.
Removed: the "Console is mainly for managing the GraphQL API" gotcha (not on the page), the "admin only" wording (reworded to the admin header shown), the invented Verify step.
Method: documentation only; no commands were run.
