---
id: computing-software.web-development.prisma.client-filtering-sorting
name: client-filtering-sorting
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-filtering-sorting, prisma, where-or-and-not, orderby-sort, case-insensitive-filter]
level: intro
status: docs-checked
description: "Filter findMany with where, combine OR, AND and NOT, filter on relations, sort with orderBy, and where case sensitivity and relevance sorting are decided."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/filtering-and-sorting.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Filtering and sorting

`where` matches by field values: `where: { email: { endsWith: "prisma.io" } }`.

Combine with `OR`, `AND`, `NOT`:

```ts
await prisma.user.findMany({
  where: {
    OR: [
      { email: { endsWith: "gmail.com" } },
      { email: { endsWith: "company.com" } },
    ],
    NOT: { email: { endsWith: "admin.company.com" } },
  },
});
```

Relation filter example: `where: { posts: { some: { published: true } } }`. The page defers relation-specific patterns to the Relation queries page.

Sort with `orderBy`, alone (`orderBy: { title: "asc" }`) or with `where`:

```ts
await prisma.post.findMany({
  where: { published: true },
  orderBy: { createdAt: "desc" },
});
```

Case sensitivity depends on the database provider and collation. On PostgreSQL, Prisma Client also supports case-insensitive filter modes on supported operators (details in the Client API reference under `mode`).

The page also mentions, without examples: sorting by related record properties or aggregates when the query shape supports it, `_relevance` ordering on PostgreSQL and MySQL (useful with full-text search), and explicit null ordering on supported databases. Use the API reference for exact syntax.

Pagination is a separate page in the same section.

## Checked

Method: 2026-11-08 read the cited filtering-and-sorting.mdx in full (raw file from the prisma/docs repo). Examples and the case-sensitivity, relation-sort, _relevance and null-ordering notes match the page; the latter three are only described there, not demonstrated. Removed: "(not read here)" caveats replaced by pointers the page itself gives, and skill-id cross-references the page does not state.
