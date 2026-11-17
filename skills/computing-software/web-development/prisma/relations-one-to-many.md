---
id: computing-software.web-development.prisma.relations-one-to-many
name: relations-one-to-many
category: computing-software
field: web-development
product: prisma
tags: [prisma-relations-one-to-many, prisma, one-to-many-relation, optional-foreign-key, list-relation-field]
level: practitioner
status: docs-checked
description: "Define one-to-many relations, make the child side optional or mandatory, reference a non-id unique field, and use composite references."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/relations/one-to-many-relations.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# One-to-many relations

One record on the parent side, zero or more on the child side. The parent has a list field and the child holds the annotated relation field and the foreign key:

```prisma
model User {
  id    Int    @id @default(autoincrement())
  posts Post[]
}

model Post {
  id       Int  @id @default(autoincrement())
  author   User @relation(fields: [authorId], references: [id])
  authorId Int
}
```

A user can have zero or more posts; a post must have an author. The only difference from one-to-one is the missing `UNIQUE` on the foreign key.

Optional versus mandatory: the list side is always mandatory (no `Post[]?`). The child side may be optional, `author User? @relation(...)` with `authorId Int?`, so a Post can exist without a User. Otherwise it is mandatory.

Reference a non-primary key: the referenced field must be unique, for example `email String @unique` on `User` and `author User @relation(fields: [authorEmail], references: [email])` on `Post` with `authorEmail String`.

Multi-field relations (relational databases only): if `User` has `@@id([firstName, lastName])`, `Post` declares `authorFirstName` and `authorLastName` and uses `fields: [authorFirstName, authorLastName], references: [firstName, lastName]`. The referenced fields must form a `@@id` or `@@unique`.

## Checked

Method: 2026-11-08 read the cited one-to-many-relations.mdx in full (raw file from the prisma/docs repo). Snippets and rules match the page. Removed the advice to set referential actions for deleting parents, which the page does not mention.
