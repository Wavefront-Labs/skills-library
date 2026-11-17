---
id: computing-software.web-development.prisma.relations-basics
name: relations-basics
category: computing-software
field: web-development
product: prisma
tags: [prisma-relations-basics, prisma, relation-fields, relation-scalar-field, relation-attribute, foreign-key-fields]
level: intro
status: docs-checked
description: "How relation fields, relation scalar fields and the @relation fields and references arguments fit together, when @relation is required, and nested writes."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/relations/index.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Relations: fields and the @relation attribute

A relation connects two models. It needs exactly two relation fields, one on each model. Relation fields exist only at the Prisma level; the relation scalar field (for example `authorId`) is the actual foreign key column.

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

`fields` lists the scalar field(s) on this model, `references` the field(s) on the other model. They must be the same number and in the same order. The referenced fields must be the other model's `@id` or a `@unique`, or together form its `@@id` or `@@unique` (MongoDB has no `@@id`). The convention for names is relation field plus `Id` (`author` and `authorId`).

`@relation` is required for one-to-one and one-to-many, for disambiguating several relations between the same models, for self-relations, and for MongoDB many-to-many. Implicit relational many-to-many does not need it.

Disambiguate with a matching name on both sides:

```prisma
writtenPosts Post[] @relation("WrittenPosts")
pinnedPost   Post?  @relation("PinnedPost")
```

On MongoDB with ObjectId, put `@db.ObjectId` on both the model id and the relation scalar.

Client usage: nested `create` under a relation field, `include: { posts: true }` to load relations, and `posts: { connect: { id: 4 } }` in an update to attach an existing record.
## Checked

Method: 2026-11-08 read the cited relations index.mdx in full (raw file from the prisma/docs repo). All claims match the page. Removed only the cross-reference to a relation-queries skill, which the page does not name.
