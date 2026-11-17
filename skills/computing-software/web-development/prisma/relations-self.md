---
id: computing-software.web-development.prisma.relations-self
name: relations-self
category: computing-software
field: web-development
product: prisma
tags: [prisma-relations-self, prisma, self-relation, follows-model, teacher-students, relation-name]
level: practitioner
status: docs-checked
description: "Write self-relations for one-to-one, one-to-many and many-to-many on one model, always with a named @relation, including the explicit Follows variant."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/relations/self-relations.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Self-relations

A relation field can reference its own model; self-relations can be 1-1, 1-n or m-n and always require the `@relation` attribute.

One-to-one (predecessor and successor): both sides use the same `@relation` name, one side is fully annotated with `fields` and `references`, the foreign key is `@unique`, and the relation cannot be required on both sides (the first record could never be created).

```prisma
model User {
  id          Int   @id @default(autoincrement())
  successorId Int?  @unique
  successor   User? @relation("BlogOwnerHistory", fields: [successorId], references: [id])
  predecessor User? @relation("BlogOwnerHistory")
}
```

One-to-many (teacher and students): no `@unique` on the foreign key, so several students can share a teacher.

```prisma
teacherId Int?
teacher   User?  @relation("TeacherStudents", fields: [teacherId], references: [id])
students  User[] @relation("TeacherStudents")
```

Many-to-many (followers): implicit for relational databases, Prisma manages the relation table.

```prisma
followedBy User[] @relation("UserFollows")
following  User[] @relation("UserFollows")
```

For extra fields use an explicit model, `Follows`, with `followedBy User @relation("followedBy", fields: [followedById], references: [id])`, `following User @relation("following", fields: [followingId], references: [id])` and `@@id([followingId, followedById])`, and on `User` the list fields `followedBy Follows[] @relation("followedBy")` and `following Follows[] @relation("following")`.

A model can combine several self-relations (teacher/students plus followers); the page's example gives each a distinct name.

## Checked

Method: 2026-11-08 read the cited self-relations.mdx in full (raw file from the prisma/docs repo). All schema snippets and rules match the page. Small edits: added the stated meaning of the 1-n case and the implicit m-n note; reworded "give each a distinct name" to what the example shows.
