---
id: computing-software.web-development.prisma.client-pagination
name: client-pagination
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-pagination, prisma, skip-take-offset, cursor-pagination, keyset-pagination]
level: intro
status: docs-checked
description: "Paginate with skip and take for page numbers or cursor plus take plus skip 1 for scalable feeds, and know when each is appropriate."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/pagination.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pagination

Prisma Client supports offset and cursor-based pagination.

Offset: `findMany({ skip: 20, take: 10 })`. Simple, good for numbered pages and shallow navigation, but it becomes more expensive as the offset grows.

Cursor: for feeds, timelines and large datasets. Fetch a page with `orderBy`, remember the last row, then pass it as the cursor and skip the cursor row itself:

```ts
const nextPage = await prisma.post.findMany({
  take: 10,
  skip: 1,
  cursor: { id: lastPost.id },
  orderBy: { id: "asc" },
});
```

Walkthrough of the docs' cursor example: first fetch `take: 10` ordered by `id` ascending; take the last element (`firstPage[firstPage.length - 1]`); if it exists, fetch the next page with `cursor: { id: lastPost.id }`, `skip: 1` and the same `orderBy`; otherwise the next page is an empty array. The example uses the same `orderBy` on both calls.

Choose offset when users need to jump directly to a numbered page; choose cursor when performance and consistency matter as the dataset grows. Related pages named by the docs: filtering and sorting, Query Insights, the Prisma Client API reference.

## Checked

Method: 2026-11-08 read the cited pagination.mdx in full (raw file from the prisma/docs repo). Claims about offset, cursor, skip 1 and when to choose each match the page. Removed: the claim that cursor on a view needs a @unique field and a cross-reference to a views skill (not on the page), and the assertion that a changed ordering breaks the cursor (the page only shows a constant orderBy). The page is short; no more detail is claimed.
