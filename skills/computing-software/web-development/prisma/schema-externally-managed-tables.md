---
id: computing-software.web-development.prisma.schema-externally-managed-tables
name: schema-externally-managed-tables
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-externally-managed-tables, prisma, tables-external, enums-external, external-tables-shadow-db, experimental-externaltables]
level: advanced
status: docs-checked
description: "Query tables owned by another service without migrating them using tables.external and enums.external in prisma.config.ts, with initShadowDb for relations."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/externally-managed-tables.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Externally managed tables (preview)

External tables can be queried by Prisma Client but are ignored by Prisma Migrate. Use cases from the docs: auth services such as Clerk or Auth0, Supabase Storage metadata tables, or tables owned by another team.

Declare them in `prisma.config.ts` and switch on the experimental flag:

```ts
export default defineConfig({
  schema: "prisma/schema.prisma",
  datasource: { url: env("DATABASE_URL") },
  experimental: { externalTables: true },
  tables: { external: ["public.users"] },
  enums: { external: ["public.role"] },
});
```

Naming: on PostgreSQL and SQL Server use the fully qualified `schema.table` (for example `auth.users`); on MySQL and SQLite only the table name. Enums can be external too.

Workflow: declare, update the schema (`npx prisma db pull` or hand-written models), `npx prisma generate`, then query, for example `prisma.users.findMany()`. When the owner changes the table, re-pull and regenerate.

Prisma does not check that your model matches the real table. That lets you expose only some columns, but you must keep the model right (db pull is the safest way).

Relations from a managed model to an external table are supported, but Migrate must know the table. Supply SQL in `migrations.initShadowDb`, run on the shadow database before all migrations, for example `CREATE TABLE public.users (id SERIAL PRIMARY KEY);`. A placeholder needs only the primary key. If no managed table has a foreign key to the external one, no SQL is needed. Relations where the external table holds the foreign key to a managed table are not managed by Prisma, since that would alter the external table.

Often combined with multi-schema (see `prisma-schema-multi-schema`) but a single schema works too.

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/data-model/externally-managed-tables pages, orm/v7): preview status, use cases, experimental.externalTables, tables.external and enums.external, naming rules per database, workflow, no structure check, initShadowDb rules, multi-schema note.

Method: documentation only; no commands were run.
