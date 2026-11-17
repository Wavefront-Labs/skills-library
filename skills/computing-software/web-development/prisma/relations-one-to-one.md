---
id: computing-software.web-development.prisma.relations-one-to-one
name: relations-one-to-one
category: computing-software
field: web-development
product: prisma
tags: [prisma-relations-one-to-one, prisma, one-to-one-relation, unique-foreign-key, optional-relation, multi-field-relation]
level: practitioner
status: docs-checked
description: "Model one-to-one relations with a unique foreign key, pick which side holds it, make either side optional or required, and use multi-field keys."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/relations/one-to-one-relations.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# One-to-one relations

At most one record on each side. The foreign key must be `@unique`, otherwise it is a one-to-many relation.

```prisma
model User {
  id      Int      @id @default(autoincrement())
  profile Profile?
}

model Profile {
  id     Int  @id @default(autoincrement())
  user   User @relation(fields: [userId], references: [id])
  userId Int  @unique
}
```

A user has zero or one profile; a profile always belongs to one user. You can reference a non-id unique field (`references: [email]` with `userEmail String @unique`).

Required versus optional: the side without a relation scalar must be optional (`profile Profile?`). The side with the scalar can be required (`profile Profile @relation(...)` and `profileId Int @unique`), meaning a User cannot be created without a Profile, or optional (`Profile?` and `profileId Int? @unique`).

You choose which side holds the `@relation` and foreign key (`profile Profile? @relation(fields: [profileId], references: [id])` with `profileId Int? @unique` on `User`, and `user User?` on `Profile`). Both layouts are valid.

Multi-field (relational databases only): when the parent has `@@id([firstName, lastName])`, the child declares both scalars, `@relation(fields: [userFirstName, userLastName], references: [firstName, lastName])`, and `@@unique([userFirstName, userLastName])`.

In MongoDB the documents reference each other by ID (the page's example stores the user's `$oid` in the profile's `userId`).

## Checked

Method: 2026-11-08 read the cited one-to-one-relations.mdx in full (raw file from the prisma/docs repo). Snippets and rules match the page. Removed the claim that changing the foreign-key side later needs a customised migration and its cross-reference (not on the page).
