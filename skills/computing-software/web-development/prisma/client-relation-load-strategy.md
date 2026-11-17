---
id: computing-software.web-development.prisma.client-relation-load-strategy
name: client-relation-load-strategy
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-relation-load-strategy, prisma, relationjoins-preview, lateral-join, join-vs-query-strategy]
level: advanced
status: docs-checked
description: "Choose relationLoadStrategy join or query per request under the relationJoins preview feature, and know what each does on PostgreSQL and MySQL."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/relation-queries.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Relation load strategies

Preview feature `relationJoins`; add it to `previewFeatures` in the generator and run `prisma generate` again. Available on PostgreSQL, CockroachDB and MySQL.

Use the top-level `relationLoadStrategy` option on any query that supports `include` or `select`:

```ts
const users = await prisma.user.findMany({
  relationLoadStrategy: "join", // or "query"
  include: { posts: true },
});
```

- `join` (default): one database query. PostgreSQL uses `LATERAL JOIN` plus JSON aggregation, so the database builds the JSON structures; MySQL uses correlated subqueries.
- `query`: one query per table, merged in the application.

Guidance from the docs: `join` is more effective in most cases because it cuts redundancy in result sets and offloads shaping to the database. There may be edge cases where `query` is faster depending on the data, so profile. Pick `query` to spare the database server and do the merging on application servers, which may be easier to scale.

Both examples in the docs set the option at the top level of `findMany`, once with `include: { posts: true }` and once with `select: { posts: true }`. The page's intro describes the option as per-query and mentions PostgreSQL, while a later paragraph lists PostgreSQL, CockroachDB and MySQL as supported.

## Checked

Method: 2026-11-08 read the cited relation-queries.mdx in full (raw file from the prisma/docs repo; only the relation-load-strategy section is used here). Flag, strategies and guidance match the page. Removed the claims that nothing changes until regenerating and that the option need only be written for query, which are inferences rather than page statements.
