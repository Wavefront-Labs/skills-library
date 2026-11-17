---
id: computing-software.web-development.prisma.client-fluent-api
name: client-fluent-api
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-fluent-api, prisma, chained-relation-calls, fluent-relation-traversal]
level: intro
status: docs-checked
description: "Traverse relations by chaining calls after findUnique, such as user.findUnique().posts(), with the single-object requirement and the two-query cost."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/relation-queries.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fluent API

Chain relation names after a query to get related records:

```ts
const postsByUser: Post[] = await prisma.user
  .findUnique({ where: { email: "alice@prisma.io" } })
  .posts();
```

The last call decides the return type. Chains can be long: `prisma.profile.findUnique({ where: { id: 1 } }).user().posts()`.

Requirement: each call before the next must return a single object (`findUnique`, or a to-one relation like `user()`). `prisma.user.findMany().posts()` is illegal because `findMany` returns a list.

Cost: the fluent call equals a `post.findMany({ where: { author: { email } } })` result, but is executed as two database queries whereas the `findMany` form runs one.

More examples from the docs: `prisma.post.findUnique({ where: { id: 1 } }).categories()` returns the categories of one post, typed `Category[]`. The page says you can chain as many calls as you like, provided each earlier call returns a single object. The page links a GitHub issue for the two-query behaviour.

## Checked

Method: 2026-11-08 read the cited relation-queries.mdx in full (raw file from the prisma/docs repo; only the fluent API section is used here). Examples, the single-object rule, the illegal findMany chain and the two-query note match the page. Removed the advice to prefer findMany or include when query count matters and its cross-reference (not on the page).
