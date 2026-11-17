---
id: computing-software.web-development.prisma.schema-table-inheritance-sti
name: schema-table-inheritance-sti
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-table-inheritance-sti, prisma, single-table-inheritance, discriminator-column, union-types-workaround]
level: practitioner
status: docs-checked
description: "Model polymorphic data with single-table inheritance: one model with optional columns and an enum discriminator, plus Omit-based types for videos and articles."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/table-inheritance.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Single-table inheritance

Prisma schema cannot express union types, so the docs show table inheritance as the workaround. Example: an activity is a video (extra `duration Int`) or an article (extra `body String`).

STI puts everything in one model with a discriminator:

```prisma
model Activity {
  id       Int          @id
  url      String       @unique
  duration Int?         // video-only
  body     String?      // article-only
  type     ActivityType // discriminator
  owner    User @relation(fields: [ownerId], references: [id])
  ownerId  Int
}

enum ActivityType {
  Video
  Article
}
```

Subtype columns must be optional, because a video row can have no `body` and an article row no `duration`.

Only one `Activity` type and one set of CRUD methods exist. Filter by discriminator: `prisma.activity.findMany({ where: { type: "Video" } })`. TypeScript still types every row as `Activity`, so both optional fields show up. For safer types, derive them with `Omit`:

```ts
type Video = Omit<Activity, "body" | "type">;
type Article = Omit<Activity, "duration" | "type">;
```

Then write mapping functions such as `activityToVideo` that copy fields and substitute a fallback (the docs use `-1` for a missing duration, `""` for a missing body), and `map` the query result through them.

The docs also point to Prisma Client extensions for a more convenient API. Per the page's trade-offs, STI can mean very wide rows with many NULL columns, and you must build the specific types yourself, whereas multi-table inheritance gives per-model typings.

## Checked

Method: 2026-11-08 read the cited table-inheritance.mdx in full (raw file from the prisma/docs repo). Schema, Omit types, fallback values and the unsupported-union-types note match the page. Replaced the cross-reference to the MTI skill with the page's own trade-off statements.
