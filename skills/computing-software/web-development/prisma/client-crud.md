---
id: computing-software.web-development.prisma.client-crud
name: client-crud
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-crud, prisma, upsert-find-or-create, createmanyandreturn, atomic-increment]
level: intro
status: docs-checked
description: "Create, read, update and delete with Prisma Client, including createMany skipDuplicates limits, the *AndReturn variants, upsert, and atomic increments."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/crud.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CRUD with Prisma Client

Create: `prisma.user.create({ data: { email, name } })`. `createMany({ data: [...], skipDuplicates: true })` returns `{ count }`; `skipDuplicates` is not supported on MongoDB, SQL Server or SQLite. `createManyAndReturn` returns the rows (PostgreSQL, CockroachDB, SQLite).

Read: `findUnique({ where: { email } })` or by `id`; `findMany()`; `findFirst({ where, orderBy })`. Add `select: { email: true, name: true }` or `include: { posts: true }`.

Update: `update({ where, data })`; `updateMany({ where, data })` returns `{ count }`; `updateManyAndReturn` (PostgreSQL, CockroachDB, SQLite). `upsert({ where, update, create })`; for findOrCreate semantics, call upsert with an empty `update`. Atomic numbers: `data: { views: { increment: 1 } }`.

Delete: `delete({ where })`, `deleteMany({ where })`, `deleteMany({})` for all rows.

Failure mode: deleting a user who has posts fails when the relation is required, with "The change you are trying to make would violate the required relation 'PostToUser' between the `Post` and `User` models." Options: make the relation optional (`author User?`, `authorId Int?`), reassign the posts first, delete posts and user together in `$transaction([deletePosts, deleteUser])`, or configure cascading deletes with referential actions (see `prisma-relations-referential-actions`).

Nested writes and relation reads: `prisma-client-nested-writes`, `prisma-client-relation-queries`.

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-client/queries/crud pages, orm/v7): create, createMany with skipDuplicates limits, the AndReturn variants and their databases, find and update calls, upsert with empty update, increment, delete calls, the required-relation error text and its four remedies.

Method: documentation only; no commands were run.
