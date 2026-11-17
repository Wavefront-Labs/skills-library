---
id: computing-software.web-development.prisma.schema-table-inheritance-mti
name: schema-table-inheritance-mti
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-table-inheritance-mti, prisma, multi-table-inheritance, delegated-types, sti-vs-mti]
level: practitioner
status: docs-checked
description: "Model polymorphism with multi-table inheritance using a parent Activity table and one-to-one child tables, and weigh it against single-table inheritance."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/table-inheritance.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multi-table inheritance (delegated types)

A parent table holds shared columns and the discriminator; each subtype has its own table with a unique foreign key back to the parent.

```prisma
model Activity {
  id      Int          @id @default(autoincrement())
  url     String
  type    ActivityType
  video   Video?
  article Article?
  owner   User @relation(fields: [ownerId], references: [id])
  ownerId Int
}

model Video {
  id         Int      @id @default(autoincrement())
  duration   Int
  activityId Int      @unique
  activity   Activity @relation(fields: [activityId], references: [id])
}
```

`Article` mirrors `Video` with `body String`. The 1-1 relations fetch subtype data. Subtype columns can be required.

Querying: `prisma.video.findMany({ include: { activity: true } })` gives subtype plus shared fields. Or start from the parent: `prisma.activity.findMany({ where: { type: "Video" }, include: { video: true } })`.

Dedicated types combine generated ones, for example `Omit<VideoDB & Activity, "type">`, with a mapper from the query result to that shape. The docs' mapper types the include result with `Prisma.validator<Prisma.VideoDefaultArgs>()` and `Prisma.VideoGetPayload`, then maps fields from both rows (for example `url: a.activity.url`, `duration: a.duration`).

Trade-offs from the docs:
- Data model: MTI is cleaner; STI makes wide rows with many NULLs.
- Performance: MTI joins parent and child to read all properties.
- Typings: MTI gives proper per-model types; STI needs them built.
- IDs: MTI rows have two ids (parent and child) that may differ, which business logic must handle.

The docs mention ZenStack as a third-party layer for polymorphism.

## Checked

Method: 2026-11-08 read the cited table-inheritance.mdx in full (raw file from the prisma/docs repo). Schema, queries, dedicated types and the four trade-offs match the page. Removed the unsupported advice to use satisfies instead of Prisma.validator in v7 and its cross-reference; the page uses Prisma.validator.
