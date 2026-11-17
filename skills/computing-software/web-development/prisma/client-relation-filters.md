---
id: computing-software.web-development.prisma.client-relation-filters
name: client-relation-filters
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-relation-filters, prisma, some-every-none, is-isnot, filter-no-related-records]
level: practitioner
status: docs-checked
description: "Filter parents by related records with some, every and none for to-many and is and isNot for to-one, plus empty and present relation checks."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/relation-queries.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Relation filters

To-many side, use `some`, `every`, `none`:

- some posts unpublished: users with at least one unpublished post
- none unpublished: users with no unpublished post
- every unpublished: users whose posts are all unpublished

```ts
await prisma.user.findMany({
  where: {
    posts: {
      none: { views: { gt: 100 } },
      every: { likes: { lte: 50 } },
    },
  },
});
```

To-one side, use `is` and `isNot`:

```ts
await prisma.post.findMany({
  where: { author: { isNot: { name: "Bob" }, is: { age: { gt: 40 } } } },
});
```

Absence and presence:
- Users with zero posts: `posts: { none: {} }`.
- Users with at least one post: `posts: { some: {} }`.
- Posts with no author: `author: null` (or `author: {}` per the docs comment).

The to-many example above applies `none` and `every` to the same `posts` relation together (no post over 100 views, all posts at most 50 likes). The page's examples also pass `include: { posts: true }` to return the related rows.

## Checked

Method: 2026-11-08 read the cited relation-queries.mdx in full (raw file from the prisma/docs repo; only the relation filters section is used here). Option names, the requirement table and examples match the page. Removed the statement that scalar filters can sit beside relation filters and the cross-reference to another skill, neither of which the page makes.
