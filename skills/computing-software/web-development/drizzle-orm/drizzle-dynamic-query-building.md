---
id: computing-software.web-development.drizzle-orm.drizzle-dynamic-query-building
name: drizzle-dynamic-query-building
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, dynamic, query-builder, composable-queries, typescript-generics]
level: advanced
status: docs-checked
description: "Build Drizzle queries in reusable pieces with $dynamic(), generic PgSelect helper functions like withPagination, and the types per statement."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/dynamic-query-building.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: lift the call-once restriction on builder methods.

By default each clause can be called once: a second `.where()` is a type error, because SQL has one WHERE. Call `.$dynamic()` on the builder to allow repeated or helper-added clauses.

```ts
function withPagination<T extends PgSelect>(qb: T, page = 1, pageSize = 10) {
  return qb.limit(pageSize).offset((page - 1) * pageSize);
}
const query = db.select().from(users).where(eq(users.id, 1));
withPagination(query, 1);                    // type error: not dynamic
withPagination(query.$dynamic(), 1);         // OK
```

Helpers may change the result type, for example adding a join:

```ts
function withFriends<T extends PgSelect>(qb: T) {
  return qb.leftJoin(friends, eq(friends.userId, users.id));
}
let q = db.select().from(users).where(eq(users.id, 1)).$dynamic();
q = withFriends(q);
```

Generic types: select `PgSelect` (or `PgSelectQueryBuilder`), insert `PgInsert`, update `PgUpdate`, delete `PgDelete`. The `...QueryBuilder` types serve standalone `new QueryBuilder()` instances, and database query builders are subclasses of them.

These types are designed for dynamic query building and can only be used in dynamic mode.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (dynamic-query-building.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
