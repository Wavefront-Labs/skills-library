---
id: computing-software.web-development.prisma.schema-map-names
name: schema-map-names
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-database-mapping, prisma, atmap-attribute, atatmap-model, enum-map-values, typescript-enum-mapped]
level: practitioner
status: docs-checked
description: "Decouple Client names from table, column and enum names with @map and @@map, and know the generated TypeScript enum keeps schema names."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/database-mapping.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mapping model, field and enum names

`@@map("table")` on a model and `@map("column")` on a field let the Client API use different names than the database. Introspecting a table `comments` gives `model comments`; rename it to `Comment` and add `@@map("comments")` and the table stays untouched. The docs recommend singular PascalCase model names.

```prisma
model Comment {
  content String @map("comment_text")
  email   String @map("commenter_email")

  @@map("comments")
}
```

Here the column `comment_text` is reached as `prisma.comment` field `content`, never as `comment_text`.

Enums take both: `@@map("comment_source_enum")` renames the enum type and `Twitter @map("comment_twitter")` renames one value.

Trap: with `@map` on enum values the generated TypeScript uses the schema names. For `PENDING @map("pending")` the generated object is `{ PENDING: "PENDING" }`, so `Status.PENDING` is `"PENDING"`, not `"pending"`. The mapping exists only in the database.

Related uses: two tables with the same name in different database schemas need unique model names plus `@@map` (see `prisma-schema-multi-schema`). Constraint and index names are a separate mechanism (see `prisma-schema-constraint-names`).

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/data-model/database-mapping pages, orm/v7): @map and @@map examples, recommended naming, enum mapping, the generated TypeScript enum keeping schema names.

Method: documentation only; no commands were run.
