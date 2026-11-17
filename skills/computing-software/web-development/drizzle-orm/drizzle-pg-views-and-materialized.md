---
id: computing-software.web-development.drizzle-orm.drizzle-pg-views-and-materialized
name: drizzle-pg-views-and-materialized
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, views, materialized-view, existing-view, refresh]
level: advanced
status: docs-checked
description: "Declare views and materialized views in Drizzle: query-builder, standalone and raw SQL forms, .existing() views, refreshMaterializedView and options."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/views.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage views from the schema.

Query-builder form infers columns:

```ts
export const customersView = pgView("customers_view").as((qb) =>
  qb.select().from(user).where(eq(user.role, "customer")));
```

A standalone `new QueryBuilder()` works the same way. For SQL the view columns must be declared:

```ts
export const newYorkers = pgView('new_yorkers', {
  id: serial('id').primaryKey(), name: text('name').notNull(), cityId: integer('city_id').notNull(),
}).as(sql`select * from ${users} where ${eq(users.cityId, 1)}`);
```

Existing views (when you have read-only access): declare columns and call `.existing()`; drizzle-kit ignores it and does not generate a create view statement.

Materialized views: `pgMaterializedView('new_yorkers').as((qb) => ...)`. Refresh at runtime:

```ts
await db.refreshMaterializedView(newYorkers);
await db.refreshMaterializedView(newYorkers).concurrently();
await db.refreshMaterializedView(newYorkers).withNoData();
```

Extended options: `.with({ checkOption: 'cascaded', securityBarrier: true, securityInvoker: true })` for views; `.using('heap')`, `.with({ fillfactor: 90, ... })`, `.tablespace('...')`, `.withNoData()` for materialized views. Parameters inside a view query are inlined rather than bound as `$1`.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (views.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
