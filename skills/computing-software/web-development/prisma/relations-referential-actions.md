---
id: computing-software.web-development.prisma.relations-referential-actions
name: relations-referential-actions
category: computing-software
field: web-development
product: prisma
tags: [prisma-relations-referential-actions, prisma, on-delete-cascade, set-null-action, restrict-vs-noaction, referential-action-defaults]
level: practitioner
status: docs-checked
description: "Set onDelete and onUpdate in @relation with Cascade, Restrict, NoAction, SetNull and SetDefault, know the defaults, per-database support and runtime failure cases."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/relations/referential-actions.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Referential actions

Defined on `@relation`, they map to foreign key constraints:

```prisma
author   User @relation(fields: [authorId], references: [id], onDelete: Cascade, onUpdate: Cascade)
```

Defaults when unset: `onDelete` is `SetNull` for optional relations and `Restrict` for mandatory ones; `onUpdate` is `Cascade` for both.

Actions:

- `Cascade`: deleting the referenced record deletes the referencing ones; updating the referenced id updates the foreign key.
- `Restrict`: blocks deleting or changing the referenced record while references exist.
- `NoAction`: like Restrict, but database dependent. PostgreSQL can defer the check within the transaction; MySQL behaves as Restrict; SQLite takes no action; SQL Server raises an error; MongoDB does nothing to related records.
- `SetNull`: sets the foreign key to NULL. Only works on optional relations; on a required relation you get a runtime error because the column is not nullable.
- `SetDefault`: sets the foreign key to its `@default`. Needs a default on the relation scalar field, otherwise a runtime error. Example: `authorUsername String? @default("anonymous")` with `onDelete: SetDefault`.

Per database: SQL Server has no `Restrict` (use `NoAction`, same result); MySQL/MariaDB do not truly support `SetDefault` (on MySQL 8+ and MariaDB 10.5+ it acts as `NoAction` and fails at runtime with a foreign key error; older versions fail with a syntax error), and Prisma warns; MongoDB has no `SetDefault`. PostgreSQL alone lets `SetNull` point at a non-nullable field, which then errors at runtime, so Prisma warns you to make the field optional in the default `foreignKeys` mode and rejects it with a validation error on other providers.

Caveats: referential actions are not supported on implicit many-to-many relations; define an explicit join model and put the actions there. With `relationMode = "prisma"`, `NoAction` adds no protection (see `prisma-relations-relation-mode`).

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/data-model/relations/referential-actions pages, orm/v7): five actions, default table, per-database support table, MySQL/MariaDB SetDefault versions, PostgreSQL SetNull warning, SQL Server Restrict, NoAction per database, SetDefault example, implicit many-to-many caveat.

Method: documentation only; no commands were run.
