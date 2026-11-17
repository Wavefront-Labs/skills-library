---
id: computing-software.web-development.prisma.client-nested-reads
name: client-nested-reads
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-relation-queries, prisma, include-vs-select, relation-count, filter-relation-list]
level: practitioner
status: docs-checked
description: "Read related records with include and nested select, avoid select plus include on one level, count relations with _count, and filter or sort included lists."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/relation-queries.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Nested reads (relation queries)

`include` adds relation records to the result: `prisma.user.findFirst({ include: { posts: true } })`. Nest it for deeper levels: `include: { posts: { include: { categories: true } } }`.

A nested `select` picks fields of a relation: `select: { name: true, posts: { select: { title: true } } }`. You may also place a `select` inside an `include` to get all parent fields and only chosen relation fields.

Rule: `select` and `include` cannot be used on the same level. Doing so throws "Please either use `include` or `select`, but not both at the same time." Put the parent field and the relation inside one `select` instead.

Relation count: `include: { _count: { select: { posts: true } } }` returns `_count: { posts: 3 }` per row (3.0.1 or later).

Filtering and sorting a relation list inside `select` or `include`:

```ts
await prisma.user.findFirst({
  include: {
    posts: { where: { published: false }, orderBy: { title: "asc" } },
  },
});
```

Load strategy: a top-level `relationLoadStrategy` option on queries with `include` or `select` chooses `join` (default, a single database query) or `query` (one query per table, joined in the application). It is a Preview feature needing the `relationJoins` preview flag, available on PostgreSQL, CockroachDB and MySQL.

## Checked

Method: 2026-11-08 compared against the Prisma docs relation-queries.mdx source (Nested reads, Relation count, Filter a list of relations). The include, select, count and filter claims match. Replaced an unstated cross-reference with the page's own load-strategy summary.
