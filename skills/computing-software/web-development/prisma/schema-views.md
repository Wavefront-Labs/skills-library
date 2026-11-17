---
id: computing-software.web-development.prisma.schema-views
name: schema-views
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-views, prisma, views-preview, view-block, readonly-view, materialized-view]
level: advanced
status: docs-checked
description: "Model database views with the view keyword under the views preview feature, introspect them to a views folder, and know the read-only and no-index limits."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/views.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Views (preview)

Enable `previewFeatures = ["views"]` in the generator. Then represent a view with the `view` keyword; each field is a column of the query result:

```prisma
view UserInfo {
  id    Int
  email String
  name  String
  bio   String
}
```

For MongoDB the id is `String @map("_id") @db.ObjectId`.

Prisma does not create views. Migrate and `db push` run no view SQL. Create the view in the database yourself, or run `migrate dev --create-only` and add the `CREATE VIEW` SQL to the migration file.

Introspection: `prisma db pull` generates `view` blocks (fields come back optional, such as `Int?`) and writes a `views` folder under the prisma directory, with a subfolder per database schema and one `.sql` file per view, for example `views/public/UserInfo.sql`. Only PostgreSQL, MySQL, SQL Server and CockroachDB are introspected; elsewhere add views by hand.

Run `prisma generate` after changing a `view`. Query like a model: `prisma.userInfo.findMany({ where: { name: "Alice" } })`.

Limits:
- Read-only: `create`, `update`, `delete` and `upsert` are not generated, even for updatable database views. Write to the underlying tables or use raw SQL.
- No `@id`/`@@id` and no `@index`/`@@index`.
- `@unique` and `@@unique` are allowed but enforced by neither database nor Prisma; they only enable relations across views, `findUnique` and cursor pagination.
- Materialized views are unsupported as a feature. Create one in the database and refresh it manually with TypedSQL.

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/data-model/views pages, orm/v7): views preview flag, view keyword, MongoDB id, create-only workflow, introspection databases and views folder, read-only rules, no @id or @index, unsafe @unique, materialized views via TypedSQL.

Method: documentation only; no commands were run.
