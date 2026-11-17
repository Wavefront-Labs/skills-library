---
id: computing-software.web-development.prisma.schema-introspection-db-pull
name: schema-introspection-db-pull
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-introspection, prisma, db-pull-workflow, db-pull-force, introspection-merge, ignore-attribute]
level: practitioner
status: docs-checked
description: "Introspect with prisma db pull, run the change-pull-generate loop without Migrate, know what a re-pull keeps, use --force, and limit scope with a restricted user or @@ignore."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/introspection.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Introspection with prisma db pull

`prisma db pull` needs the connection URL in the config `datasource`. It reads the URL, connects, reads tables, columns and other structures, and writes the data model (or merges into the existing schema). On SQL it maps tables to models, columns to fields, indexes and constraints to attributes. On MongoDB it samples documents in each collection to derive the model; embedded types become composite types, and an index is only mapped if some document has a field in it.

Workflow when you migrate with plain SQL or another tool: change the database, run `prisma db pull`, run `prisma generate`, use the Client. Repeatable indefinitely.

Re-pulling on relational databases merges with your schema and preserves: model and enum block order, comments, `@map` and `@@map`, `@updatedAt`, `@default(cuid())` and `@default(uuid())` (Prisma-level functions) and custom `@relation` names. The database decides field order within models and enum value order; enums are listed below models. Only relations backed by a real foreign key are picked up.

MongoDB: introspection is meant to be done once for the initial model; repeating it loses custom changes.

Force overwrite: `npx prisma db pull --force` ignores the existing schema and writes only what the database holds. Use it to start from scratch or when the existing schema is invalid and blocks introspection.

Subsets: not officially supported. Introspect as a database user that sees only the wanted tables. To keep models out of the generated Client, add `@@ignore` to the model.

Attribute order written: block level `@@id`, `@@unique`, `@@index`, `@@map`; field level `@id`, `@unique`, `@default`, `@updatedAt`, `@map`, `@relation` (the order `prisma format` mirrors). Fields are listed in column order.

## Checked

Method: 2026-11-08 read the cited introspection.mdx in full (raw file from the prisma/docs repo). Workflow, merge-preservation list, --force use cases, subset workaround and attribute order match the page. Reworded "reads tables, columns and constraints" to the page's "reads tables, columns and other structures"; claims otherwise unchanged.
