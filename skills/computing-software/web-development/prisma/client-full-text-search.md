---
id: computing-software.web-development.prisma.client-full-text-search
name: client-full-text-search
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-full-text-search, prisma, fulltextsearchpostgres-preview, search-filter, relevance-ordering]
level: practitioner
status: docs-checked
description: "Search text fields with the search filter and order by _relevance, enabling the fullTextSearchPostgres preview feature on PostgreSQL."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/full-text-search.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Full-text search in Prisma Client

Supported on MySQL, and on PostgreSQL with the `fullTextSearchPostgres` preview feature (the page carries a preview badge):

```prisma
generator client {
  provider        = "prisma-client"
  output          = "./generated"
  previewFeatures = ["fullTextSearchPostgres"]
}
```

Re-generate the client afterwards with `npx prisma generate`.

Search a field with the `search` filter:

```ts
const posts = await prisma.post.findMany({
  where: { body: { search: "cat | dog" } },
});
```

Order by relevance on supported databases:

```ts
const posts = await prisma.post.findMany({
  orderBy: {
    _relevance: { fields: ["title"], search: "database", sort: "desc" },
  },
});
```

`_relevance` takes `fields`, `search` and `sort`. The page is brief: the exact `search` operator syntax and full `_relevance` options are in the Client API reference (`#search`), which this skill does not cover.

On PostgreSQL the `search` filter wraps built-in `tsvector` matching. For search-engine-style ranking the page points to Prisma ORM 8 and its ParadeDB extension (BM25, relevance scores, fuzzy, phrase and proximity queries via `pg_search`); that is a different query builder API and is not covered here.

## Checked

Method: 2026-11-08 read the cited full-text-search.mdx in full (raw file from the prisma/docs repo). Preview flag, generator block, search filter and _relevance examples match the page. Removed: the claim that full text search is not enabled for MongoDB and the reference to a schema @@fulltext index skill (neither is on the page), and the troubleshooting checklist (an inference; only the enable-then-generate steps are stated). Added the page's tsvector and ParadeDB note.
