---
id: computing-software.web-development.prisma.schema-index-length-sort-map
name: schema-index-length-sort-map
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-index-arguments, prisma, index-length-mysql, index-sort-order, index-map-name, sqlserver-clustered]
level: practitioner
status: docs-checked
description: "Tune indexes and constraints with the length, sort, map and clustered arguments, and know which database and attribute supports each one."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/indexes.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Index arguments: length, sort, map, clustered

Arguments on `@id`, `@@id`, `@unique`, `@@unique` and `@@index`:

- `length` (MySQL only, on `String` and `Bytes`): MySQL needs a prefix length when the full value exceeds its index size limit. `id String @id @db.VarChar(3000)` is rejected by Prisma; `id String @id(length: 100) @db.VarChar(3000)` indexes the first 100 characters. Compound form: `@@id([id_1(length: 100), id_2(length: 10)])`. Migrate creates these and introspection reads them.
- `sort` (`Asc` or `Desc`): on `@unique`, `@@unique` and `@@index` in all databases, plus `@id` and `@@id` in SQL Server. PostgreSQL cannot set sort on unique constraints, only on indexes; the workaround is `CREATE UNIQUE INDEX "unique_index_desc" ON "Unique" ("unique" DESC)`. Examples: `@unique(sort: Desc)`, `@@unique([unique_1(sort: Desc), unique_2])`, and combined `@unique(sort: Desc, length: 42)`.
- `clustered` (SQL Server only): `id Int @id(clustered: false)` yields `PRIMARY KEY NONCLUSTERED`. Defaults: `@id` and `@@id` true; `@unique`, `@@unique`, `@@index` false. A table can have at most one clustered index.
- `map` (all databases): custom constraint or index name, otherwise a default such as `Post_title_idx`. `@@index([title], map: "my_custom_index_name")`, `email String @unique(map: "unique_user_email")`, `@@index([author, createdAt], map: "posts_author_date_idx")`.

Mixed example from the docs: `@@id([title(length: 100, sort: Desc), abstract(length: 10)])` and `@@index([author, created_at(sort: Desc)])`.

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/data-model/indexes pages, orm/v7): length (MySQL only), sort availability by database and the PostgreSQL unique-index workaround, clustered (SQL Server) defaults and one-clustered-index rule, map and its default name, mixed example.

Method: documentation only; no commands were run.
