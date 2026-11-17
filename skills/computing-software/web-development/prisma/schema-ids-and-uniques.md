---
id: computing-software.web-development.prisma.schema-ids-and-uniques
name: schema-ids-and-uniques
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-ids-uniques, prisma, composite-id, atid-attribute, unique-constraint-name, mongodb-objectid]
level: practitioner
status: docs-checked
description: "Choose between @id, @@id and @unique for model identity, name composite keys, add @@unique and @@index, and follow the MongoDB @map(_id) rules."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/models.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IDs, unique constraints and indexes

A model has only one ID. In relational databases it can be a single field (`id Int @id @default(autoincrement())`) or several via `@@id([firstName, lastName])`. If there is no `@id` or `@@id` you must have a mandatory `@unique` field or a `@@unique` block, and that unique field must be required (not optional).

A composite ID is addressed in Prisma Client under the generated name `firstName_lastName`. Rename it with the `name` argument:

```prisma
@@id(name: "fullName", fields: [firstName, lastName])
```

`@@unique([authorId, title])` creates a composite unique; it can also be named, for example `@@unique(name: "authorTitle", [authorId, title])` as the docs write it. Single-field uniqueness is `email String @unique`. Indexes use `@@index([title, content])`. A custom primary key, unique or index name in the database is set through the database mapping options.

MongoDB: the ID must be a single field with `@id` and `@map("_id")`. For an auto-generated ObjectId use `id String @id @default(auto()) @map("_id") @db.ObjectId`; for a value such as a username, `id String @id @map("_id")`. MongoDB does not support `@@id`, so composite IDs are impossible. Composite types support unique and index constraints on nested fields with dot notation, for example `@@unique([email, address.number])` and `@@index([address.city.name])`.

Limitation stated by the page: every model must have at least one unique identifier (`@id`, `@@id`, `@unique` or `@@unique`).

## Checked

Method: 2026-11-08 read the cited models.mdx in full (raw file from the prisma/docs repo). ID rules, composite ID naming, @@unique naming, @@index, MongoDB rules and the dot-notation examples match the page. Reworded the "failure mode" line to the page's own limitation statement, which says "must have" rather than "invalid".
