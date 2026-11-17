---
id: computing-software.web-development.prisma.schema-fulltext-index
name: schema-fulltext-index
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-fulltext-index, prisma, fulltextindex-preview, atatfulltext, mysql-fulltext]
level: practitioner
status: docs-checked
description: "Add MySQL and MongoDB full text indexes with the @@fulltext attribute behind the fullTextIndex preview feature, including sort on MongoDB."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/indexes.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Full text indexes (@@fulltext)

Available for MySQL and MongoDB through the `fullTextIndex` preview feature. Enable it in the generator:

```prisma
generator client {
  provider        = "prisma-client"
  output          = "./generated"
  previewFeatures = ["fullTextIndex"]
}
```

Declare the index on the fields to be searched:

```prisma
model Post {
  id      Int    @id
  title   String @db.VarChar(255)
  content String @db.Text

  @@fulltext([title, content])
}
```

Behaviour: `prisma db pull` adds existing full text indexes to the schema, and Prisma Migrate creates new ones in the database.

MongoDB: the same `@@fulltext` works, and you can pass `sort` on a field to order it in the index, for example `@@fulltext([title(sort: Desc), content])`, with a `String @id @map("_id") @db.ObjectId` id. Warning from the docs: Prisma Client's full text search commands are not enabled for MongoDB yet, so this only manages the index.

For querying full text on supported databases use the client search feature rather than this attribute (see `prisma-client-full-text-search`).

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/data-model/indexes pages, orm/v7): fullTextIndex preview flag, @@fulltext example, db pull and Migrate behaviour, MongoDB sort argument, MongoDB client search warning.

Method: documentation only; no commands were run.
