---
id: computing-software.web-development.prisma.client-nested-writes
name: client-nested-writes
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-nested-writes, prisma, connect-or-create, nested-create-many, set-empty-disconnect, nested-upsert]
level: practitioner
status: docs-checked
description: "Write related records in one transaction with nested create, createMany, connect, connectOrCreate, disconnect, set, update, upsert and deleteMany, and know the createMany limits."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/relation-queries.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Nested writes

A nested write changes several tables in one Client call with transactional guarantees: if any part fails (user created, posts fail) everything rolls back. Any nesting depth the data model allows. Available on relation fields in create and update queries.

Operations on a relation field, shown on `user.posts` or `post.author`:

- `create: [{ title: "..." }, ...]` creates and links; can nest further, such as `categories: { create: { name: "Easy cooking" } }`.
- `createMany: { data: [...] }` with `skipDuplicates` option. Cannot nest more creates and does not support many-to-many; in a has-one case you set the foreign key yourself, for example `{ authorId: 9 }`.
- `connect: [{ id: 8 }, { id: 9 }]` links existing records; throws if any is not found.
- `connectOrCreate: { where: { email }, create: { ... } }`.
- `disconnect: [{ id: 12 }]` for lists, `disconnect: true` for a single optional relation.
- `set: []` disconnects all records of a one-to-many.
- `deleteMany: {}` deletes all related; `deleteMany: { published: false }` or `deleteMany: [{ id: 7 }]` deletes some.
- `updateMany: { where, data }`, `update: { where, data }`, and `upsert: { create, update }`.

`create` versus `createMany` summary: create supports nesting and many-to-many; createMany supports `skipDuplicates`. Prefer nested `create` unless you need `skipDuplicates`.

Limits: top-level `createMany()` and `createManyAndReturn()` cannot create relations, so you cannot create many users with their posts in one call. Workaround: create the referenced rows first (for example `createManyAndReturn` with `select: { id: true }`), then create rows using those ids. To create everything in one database query use `$transaction` or TypedSQL.

## Checked

Method: 2026-11-08 compared against the Prisma docs relation-queries.mdx source (Nested writes sections). Operations, the create versus createMany table and the createMany limits match the page; no changes to the technical content.
