---
id: computing-software.web-development.prisma.relations-relation-mode
name: relations-relation-mode
category: computing-software
field: web-development
product: prisma
tags: [prisma-relations-relation-mode, prisma, relationmode-prisma, foreignkeys-mode, planetscale-no-foreign-keys, emulated-referential-actions]
level: advanced
status: docs-checked
description: "Choose relationMode foreignKeys or prisma, understand which constraints and actions are emulated, and what changes for introspection, migrations and index warnings."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/relations/relation-mode.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Relation mode: foreignKeys versus prisma

Set it on the datasource:

```prisma
datasource db {
  provider     = "mysql"
  relationMode = "prisma"
}
```

`foreignKeys` is the default for every relational connector: the database enforces relations with foreign keys, constraints and referential actions. `prisma` emulates some of that in Prisma Client and is the only option (and default) for MongoDB. Use it for databases without foreign keys, such as PlanetScale without native foreign key constraints, or when you choose not to use them. Where the database supports foreign keys the docs say it is usually the better choice, because emulation costs extra queries.

What `prisma` mode emulates:

- Constraints on update only: updating a record requires the related record to exist. On create nothing is checked, so invalid data can be created.
- Referential actions on update and delete. Support table: `Cascade`, `Restrict` and `SetNull` everywhere; `NoAction` everywhere except PostgreSQL and SQLite (use `Restrict`); `SetDefault` nowhere.
- Applies only to Prisma Client queries, not to raw queries.
- Error text differs: a message about violating "the required relation" instead of "Foreign key constraint failed".

Tooling effects: `db pull` in `prisma` mode does not add `@relation` automatically; add them once by hand and later pulls keep them. Migrate and `db push` create no foreign keys and no foreign-key indexes, so add `@@index([userId])` (or a `@unique`, `@@unique`, `@@id`) yourself. Without it `prisma format` and `prisma validate` warn that relation fields lose the index normally created under the hood.

Switching modes: from `foreignKeys` to `prisma`, the next Migrate or `db push` removes the foreign keys. If the new database has no foreign keys at all, old migration history that creates them may fail on rerun, so the docs suggest deleting the migrations directory; for PlanetScale they suggest `db push`. From `prisma` to `foreignKeys` the database must support foreign keys, and the next migration creates them.

## Checked

Method: 2026-11-08 read the cited relation-mode.mdx in full (raw file from the prisma/docs repo). Defaults, emulation scope, the referential-action support table, index warning, introspection and switching guidance all match the page. No claims removed.
