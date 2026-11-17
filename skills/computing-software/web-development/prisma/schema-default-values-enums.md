---
id: computing-software.web-development.prisma.schema-default-values-enums
name: schema-default-values-enums
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-defaults-enums, prisma, default-attribute, enum-block, autoincrement-default, json-default]
level: practitioner
status: docs-checked
description: "Set @default values (static, lists, now, uuid, cuid, autoincrement, escaped JSON) and declare enum blocks, with connector caveats."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/models.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Defaults and enums

`@default` sets a default for scalar fields. Allowed forms:

- static values: `5`, `"Hello"`, `false`
- lists: `[5, 6, 8]`, `["Hello", "Goodbye"]`
- functions: `now()`, `uuid()`, `cuid()`, plus `autoincrement()` and `auto()` (the MongoDB ObjectId generator)
- JSON as an escaped string: `data Json @default("{ \"hello\": \"world\" }")`

```prisma
model Post {
  id        Int      @id @default(autoincrement())
  createdAt DateTime @default(now())
  published Boolean  @default(false)
}
```

`@default(false)` is short for `@default(value: false)`. The page lists `now()`, `uuid()`, `cuid()`, `autoincrement()` and `auto()` (MongoDB ObjectId) as common functions and sends you to the schema reference ("attribute functions") for connector support, which this skill does not cover.

Enums use an `enum` block, available when the database supports them (the page links to the database features table):

```prisma
model User {
  id   Int  @id @default(autoincrement())
  role Role @default(USER)
}

enum Role {
  USER
  ADMIN
}
```

An enum member or name can be remapped with `@map` and `@@map`. Enums are scalar types, so they map to columns.

## Checked

Method: 2026-11-08 read the cited models.mdx in full (raw file from the prisma/docs repo). The allowed default forms, the escaped JSON default, the enum example and the @map/@@map note match the page. Removed the claim about uuid and cuid being Prisma-level and the dbgenerated remark with its cross-reference (not on this page); connector support is deferred to the schema reference as the page does.
