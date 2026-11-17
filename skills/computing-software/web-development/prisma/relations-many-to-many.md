---
id: computing-software.web-development.prisma.relations-many-to-many
name: relations-many-to-many
category: computing-software
field: web-development
product: prisma
tags: [prisma-relations-many-to-many, prisma, implicit-many-to-many, explicit-many-to-many, relation-table-convention, mongodb-id-arrays]
level: practitioner
status: docs-checked
description: "Choose implicit or explicit many-to-many relations, follow the _AToB relation table convention for db pull, and model MongoDB with ID arrays."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/relations/many-to-many-relations.mdx", "https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/relations/index.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Many-to-many relations

Implicit: Prisma manages a hidden relation table. Preferred unless you need extra data on the link.

```prisma
model Post {
  id         Int        @id @default(autoincrement())
  categories Category[]
}

model Category {
  id    Int    @id @default(autoincrement())
  posts Post[]
}
```

Rules: both models need a single `@id` (no multi-field ID, and `@unique` cannot stand in for `@id`); no `@relation` needed unless disambiguating; do not use `fields`, `references`, `onUpdate` or `onDelete`. Use `@relation("MyRelationTable")` on both sides to customise the table name.

Convention so `prisma db pull` recognises an implicit table: name `_CategoryToPost` (underscore, model names in alphabetical order, `To`), columns `A` (foreign key to the alphabetically first model) and `B`, a unique index on both columns and a non-unique index on `B`.

Explicit: the relation table is a model you define, used when you need to store extra metadata in it (the page's example adds `assignedAt` and `assignedBy`); the index page also says an explicit relation is needed if you want a multi-field ID or `@unique` in place of `@id`:

```prisma
model CategoriesOnPosts {
  post       Post     @relation(fields: [postId], references: [id])
  postId     Int
  category   Category @relation(fields: [categoryId], references: [id])
  categoryId Int
  assignedAt DateTime @default(now())
  assignedBy String
  @@id([postId, categoryId])
}
```

Writes nest one level deeper: `categories: { create: [{ assignedBy: "Bob", category: { connect: { id: 9 } } }] }`. Filter with `categories: { some: { category: { name: "..." } } }`.

MongoDB has no relation table: each side stores an ID array (`categoryIDs String[] @db.ObjectId`) and uses `@relation(fields: [categoryIDs], references: [id])`. Query with `categoryIDs: { hasSome: [id1, id2] }`.

## Checked

Method: 2026-11-08 read both cited pages in full (many-to-many-relations.mdx and relations index.mdx, raw files from the prisma/docs repo). Snippets, implicit rules, table conventions and MongoDB notes match. Reworded the explicit-relation guidance to what the pages state; the page says "Use implicit unless you need to store additional metadata", and "Preferred" is the skill's paraphrase of that.
