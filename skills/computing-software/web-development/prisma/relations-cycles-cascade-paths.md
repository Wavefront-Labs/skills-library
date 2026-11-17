---
id: computing-software.web-development.prisma.relations-cycles-cascade-paths
name: relations-cycles-cascade-paths
category: computing-software
field: web-development
product: prisma
tags: [prisma-relations-cycles-cascade-paths, prisma, sql-server-cascade-cycle, mongodb-noaction-self-relation, multiple-cascade-paths]
level: advanced
status: docs-checked
description: "Fix schema validation errors for self-relation cycles, three-model cycles and multiple cascade paths on SQL Server and MongoDB by setting NoAction on one relation."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/relations/referential-actions.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cascade cycles on SQL Server and MongoDB

SQL Server refuses cascading actions when the relation chain forms a cycle or has several cascade paths. MongoDB needs `NoAction` for self-relations and for cycles between three models (it uses `relationMode = "prisma"` by default). Prisma validates the data model before generating SQL and names the problem relation.

Self-relation. This fails:

```prisma
model Employee {
  id        Int        @id @default(autoincrement())
  manager   Employee?  @relation(name: "management", fields: [managerId], references: [id])
  managees  Employee[] @relation(name: "management")
  managerId Int?
}
```

with "A self-relation must have `onDelete` and `onUpdate` referential actions set to `NoAction` in one of the @relation attributes." The implicit defaults (`SetNull` and `Cascade`) create the cycle. Add both explicitly:

```prisma
manager Employee @relation(name: "management", fields: [managerId], references: [id], onDelete: NoAction, onUpdate: NoAction)
```

Defaults for such relations depend on the scalar fields: if all are optional, `onDelete` is `SetNull`; if at least one is required, `NoAction`. `onUpdate` is `Cascade` either way.

Three-model cycle (Chicken, Egg, Fox): the error reads "Reference causes a cycle ... Cycle path: Chicken.egg -> Egg.predator -> Fox.meal". The default `onUpdate: Cascade` creates it. Set `onUpdate: NoAction` on any one relation in the cycle, for example `egg Egg @relation(fields: [eggId], references: [id], onUpdate: NoAction)`.

Multiple cascade paths (SQL Server only): `Comment` reaches `User` directly through `writtenBy` and through `Post.author`. The error says the actions cascade "through multiple paths"; break one by setting `onUpdate: NoAction` (the docs example does it on `writtenBy`).

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/data-model/relations/referential-actions pages, orm/v7): SQL Server and MongoDB rules, self-relation error and fix, default table, three-model cycle, multiple cascade paths on SQL Server.

Method: documentation only; no commands were run.
