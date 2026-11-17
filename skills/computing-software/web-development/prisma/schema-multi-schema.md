---
id: computing-software.web-development.prisma.schema-multi-schema
name: schema-multi-schema
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-multi-schema, prisma, atatschema-attribute, datasource-schemas-array, same-table-name-two-schemas]
level: advanced
status: docs-checked
description: "Use several database schemas on PostgreSQL, CockroachDB or SQL Server with the datasource schemas list and @@schema, including name conflicts and moving models."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/multi-schema.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multiple database schemas

Only PostgreSQL, CockroachDB and SQL Server; not SQLite or MySQL. List the names in the datasource and tag each model or enum:

```prisma
datasource db {
  provider = "postgresql"
  schemas  = ["base", "shop"]
}

model User {
  id     Int     @id
  orders Order[]
  @@schema("base")
}
```

Order and the `Size` enum in the example use `@@schema("shop")`. Foreign keys across schemas work.

The connection string stays unchanged. Its `schema` value is the default schema for the Client and raw queries; all other Client queries use the schema of the model or enum queried.

Same table name in two schemas: give models unique names and map them back, for example `BaseConfig` with `@@map("Config")` plus `@@schema("base")`, and `UserConfig` likewise with `"users"`. Introspection (`prisma db pull`) otherwise reports a validation error naming the conflict; fix it by renaming the introspected models with the `@map` attribute.

Migrations: `prisma migrate dev --name add_profile` and `db push` work. Moving a model or enum to another schema deletes it from the source schema and creates a new one in the target.

Queries need no syntax change, for example `prisma.order.findMany({ where: { user: { id: 42 } } })`.

For tables owned by another service, see `prisma-schema-externally-managed-tables`.

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/data-model/multi-schema pages, orm/v7): supported databases, schemas list, @@schema, connection-string schema, same-name tables and @@map, migrate dev and db push, introspection conflict fix, move behaviour, query example. Removed an unconfirmed data-loss inference.

Method: documentation only; no commands were run.
